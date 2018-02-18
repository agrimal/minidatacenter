#!/opt/minidc/python-venv/bin/python

import yaml, time, os, shlex
from pylxd import Client
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

ct_list = []
ct_config = {}
ct_source = {}
network_config = {}
path = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(os.path.join(path, 'templates')))
client = Client()

# Create the list of containers to create with parameters filled in config.yml file
with open('../config.yml', 'r') as stream:
    try:
        config = yaml.load(stream)
        for parameter, value in config["containers_config"].items():
            ct_config[parameter] = value
        for parameter, value in config["containers_source"].items():
            ct_source[parameter] = value
        for container_type, container in config["containers"].items():
            for container_name, ip_dict in container.items():
                ct_list.append(
                      { 'name': container_name,
                        'architecture': 'x86_64',
                        'profiles': ['default'],
                        'config': ct_config,
                        'source': ct_source
                      })
        for network in config["networks"]:
            network_config[network['name']] = network
        dns_first_ip = config['dns_first_ip']
        dns_second_ip = config['dns_second_ip']
    except yaml.YAMLError as e:
        print(e)

# For each container we want to create
for container in ct_list:
    # We check a container with the same name already exists
    if (client.containers.exists(container['name'])):
        print('Error, container', container['name'], 'already exists, skipping...')
    # If not, we create and start the container
    else:
        print('Creating container', container['name'])
        ct = client.containers.create(container, wait=True)
        ct.start(wait=True)
        # We remove the default netplan configuration file
        cmd = "sh -c '/bin/rm /etc/netplan/*.yaml'"
        ret = ct.execute(shlex.split(cmd))
        if (ret[0] != 0):
            print("Error :", cmd, ret)
        # We configure the network
        template = env.get_template('netplan_config.yaml')
        print(template.render(network_config = network_config,
                              container_name = container['name'],
                              container_config = config["containers"],
                              dns_first_ip = dns_first_ip,
                              dns_second_ip = dns_second_ip))
