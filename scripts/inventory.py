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
    import yaml, json, os, sys, re
except ImportError as e:
    raise ImportError('Error importing modules...')

container_list = []

# We get absolute path of this file
path = os.path.dirname(os.path.abspath(__file__))

# We initialise the inventory dictionary
inventory = {}
inventory['all'] = {}
inventory['all']['children'] = []
inventory['all']['hosts'] = []
inventory['all']['vars'] = {}
inventory['_meta'] = {}
inventory['_meta']['hostvars'] = {}

# We open the config.yml file
with open(path + '/../config.yml', 'r') as stream:
    try:
        # We load the config.yml file
        config = yaml.load(stream)

        # [all_containers]
        # Common variables to all containers
        for variable, value in config['all_containers'].items():
            inventory['all']['vars'][variable] = value

        inventory['all']['vars']['all_hosts_ips'] = []
        for group in config['containers']:
            for container in config['containers'][group]:
                container_param = { 'name' : container }
                container_ips = []
                for network, container_ip in config['containers'][group][container].items():
                    for net in config['networks']:
                        if net['name'] == network:
                            container_ips.append( container_ip + re.sub('^.*(/.*)$', '\\1', net['cidr_ip']) )
                container_param.update( { 'ip' : container_ips } )
                inventory['all']['vars']['all_hosts_ips'].append( container_param )  
        # [containers]
        # For each container group
        for container_group, container_dict in config['containers'].items():
            inventory['all']['children'].append(container_group)
            inventory[container_group] = {}
            inventory[container_group]['hosts'] = []
            inventory[container_group]['children'] = []

            # For each container
            for container_name, container_ip_dict in container_dict.items():

                container_list.append(container_name)

                # We put the container name in container_group:'hosts'
                inventory[container_group]['hosts'].append(container_name)

                inventory['_meta']['hostvars'][container_name] = {}

                # We put the container ip in '_meta':'hostvars':container_name:'ansible_host'
                inventory['_meta']['hostvars'][container_name]['ansible_host'] = ( 
                    config['containers'][container_group][container_name]
                    [config['all_containers']['ansible_network']])

                inventory['_meta']['hostvars'][container_name]['networks'] = []
                for network in config['networks']:
                    if network['name'] in config['containers'][container_group][container_name]:
                        inventory['_meta']['hostvars'][container_name]['networks'].append(network)

        # [services]
        # For each service
        for service in config['services']:

            service_tag = re.sub('_config', '', service)

            # For each container declared in [containers]
            for container in container_list:
                # We put the variables from [service][vars] in [_meta]['hostvars'][container]
                for variable, value in config['services'][service_tag + '_config']['vars'].items():
                    inventory['_meta']['hostvars'][container][service_tag + '_' + variable] = value

            # For each container in [services][service]
            for container_name, variables_dict in config['services'][service].items():

                # If the container is declared in [containers][group]
                if container_name in config['containers'][service_tag + '_hosts']:
                    # We store it's own variables in [_meta]['hostvars'][container]
                    for variable, value in config['services'][service_tag + '_config'][container_name].items():
                        inventory['_meta']['hostvars'][container_name][service_tag + '_' + variable] = value
                # Else if this is the 'vars' section
                elif container_name == 'vars':
                    pass
                # Else there is a problem :
                # The container is declared in [services][service] but not in [containers][group}
                else:
                    print('Error in config.yml :\n' + container_name,
                          'is declared in [services]['+ service_tag + '_config]'
                          ' section but is not declared in [containers][' +
                          service_tag + '_hosts] section.')
                    sys.exit(1)
                
        print(json.dumps(inventory, indent=4, sort_keys=True))
        #print(yaml.dump(inventory, default_flow_style=False)) 

    except yaml.YAMLError as e:
        print(e)        
