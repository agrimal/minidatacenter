%%SHEBANG%%
#
# Copyright (c) 2018 Aurélien Grimal
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import yaml, os, shlex, re, sys
    from pylxd import Client
    #import time
    #from collections import defaultdict
    from jinja2 import Environment, FileSystemLoader
except ImportError as e:
    raise ImportError('Error importing modules...')

DEBUG = True

ct_config = {}
ct_source = {}
network_config = {}
ct_list_for_create = []
ct_network = {}
# We get absolute path of this file
path = os.path.dirname(os.path.abspath(__file__))
# We load files in the 'templates' directory for Jinja2
env = Environment(loader=FileSystemLoader(os.path.join(path, 'templates')))
# We connect to LXD API
client = Client()

#
# Create the list of containers to launch with parameters filled in config.yml file
# We get every section of config.yml in a separate dictionary
#
with open(path + '/../config.yml', 'r') as stream:
    try:
        config = yaml.load(stream)
        for parameter, value in config["containers_config"].items():
            # Used by the ct_list_for_create list
            ct_config[parameter] = value
        for parameter, value in config["containers_source"].items():
            # Used by the ct_list_for_create list
            ct_source[parameter] = value
        for network in config["networks"]:
            # Contains every network
            network_config[network['name']] = network
        for container_type, container_dict in config["containers"].items():
            for container_name, ip_dict in container_dict.items():
                # Each dictionary of this list is given to the client.containers.create() method
                ct_list_for_create.append(
                      { 'name': container_name,
                        'architecture': 'x86_64',
                        'profiles': ['default'],
                        'config': ct_config,
                        'source': ct_source
                      })
                # Contains the IP of each container
                ct_network[container_name] = ip_dict
        ssh_public_key = config['ansible_ssh_public_key']
    except yaml.YAMLError as e:
        print(e)

if DEBUG:
    print('ct_config :\n', ct_config)
    print('\nct_source :\n', ct_source)
    print('\nct_list_for_create :\n', ct_list_for_create)
    print('\nnetwork_config :\n', network_config)
    print('\nct_network :\n', ct_network)
    print('\nssh_public_key :\n', ssh_public_key)

# We don't need these anymore
del ct_config, ct_source

#
# We test if the SSH public key exists
#
ssh_pubkey = ''
try:
    with open(ssh_public_key, 'r') as f:
        ssh_pubkey = f.read()
except IOError as e:
    print('Error : problem opening SSH public key :', e)
    sys.exit(1)

#
# For each container we want to create
#
for container in ct_list_for_create:
    container_name = container['name']
    # We check if a container with the same name already exists
    if client.containers.exists(container_name) and not DEBUG:
        print('Error, container', container_name, 'already exists, skipping...')
    # If not, we create, start and configure the container
    else:
        if not DEBUG:
            # We create and start the container
            print('Creating container', container_name, "...")
            ct = client.containers.create(container, wait=True)
            ct.start(wait=True)
            # We remove the default netplan configuration file
            ret = ct.execute(shlex.split("sh -c '/bin/rm /etc/netplan/*.yaml'"))
            if ret[0] != 0:
                print("Error :", ret)
        # For each network declared in the 'networks' section
        for network_name, network_parameters_dict in network_config.items():
            # If the network is also declared in the 'containers' section
            if network_name in ct_network[container_name]:
                # We add the CIDR mask to the end of the container IP (netplan needs it)
                ct_network[container_name][network_name] = (ct_network[container_name][network_name]
                           + re.sub('^.*(/[0-9]{1,2})$', '\\1', network_parameters_dict['cidr_ip']))
        # We read the template for netplan configuration file
        template = env.get_template('netplan_config.yaml.j2')
        # We render it
        netplan = template.render(network_config = network_config,
                                  container_name = container['name'],
                                  container_config = ct_network[container['name']])
        # Due to a Jinja2 bug with '{%+' and '+%}', we need to remove manually some empty lines
        newnetplan = os.linesep.join([string for string in netplan.splitlines() if string.strip()])
        if DEBUG:
            print('\nnetplan of', container_name, ':\n', newnetplan)
            print('\nbuilt with :')
            print('\n\tnetwork_config :\n', network_config)
            print('\n\tcontainer_name :\n', container_name)
            print('\n\tcontainer_config :\n', ct_network[container['name']])
        else:
            # We send the file into the container
            ct.files.put('/etc/netplan/config.yaml', newnetplan)
            # We send the SSH public key into the container
            ret = ct.execute(['mkdir','/root/.ssh'])
            if ret[0] != 0:
                print("Error :", ret)
            ct.files.put('/root/.ssh/authorized_keys', ssh_pubkey)
            # We restart the container
            ct.restart(wait=True)
            # We install openssh-server
            ret = ct.execute(['apt','install','-y','openssh-server'])
            if ret[0] != 0:
                print("Error :", ret)
