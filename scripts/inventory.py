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
    import yaml, json, os, sys
except ImportError as e:
    raise ImportError('Error importing modules...')

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

        # Common variables to all containers
        for variable, value in config["all_containers"].items():
            inventory['all']['vars'][variable] = value

        # For each container group
        for container_group, container_dict in config["containers"].items():
            inventory['all']['children'].append(container_group)
            inventory[container_group] = {}
            inventory[container_group]['hosts'] = []
            inventory[container_group]['children'] = []

            # For each container
            for container_name, container_ip_dict in container_dict.items():
                # We put the container name in /container_group/'hosts'/
                inventory[container_group]['hosts'].append(container_name)
                inventory['_meta']['hostvars'][container_name] = {}
                # We put the container ip in /'_meta'/'hostvars'/container_name/'ansible_host'/
                inventory['_meta']['hostvars'][container_name]['ansible_host'] = ( 
                    config['containers'][container_group][container_name][config['ansible_network']])
                

        print(json.dumps(inventory, indent=4, sort_keys=True))
        #print(yaml.dump(inventory, default_flow_style=False)) 

    except yaml.YAMLError as e:
        print(e)        
