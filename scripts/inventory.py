#!/opt/minidc/python-venv/bin/python
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
inventory = {}
inventory['all'] = {}
inventory['all']['hosts'] = ['toto.com']
inventory['all']['children'] = {}

# Prevent pyyaml from dumping None to null
#def represent_none(self, _):
#    return self.represent_scalar('tag:yaml.org,2002:null', '')
#
#yaml.add_representer(type(None), represent_none)

with open(path + '/../config2.yml', 'r') as stream:
    try:
        config = yaml.load(stream)
        for container_type, container_dict in config["containers"].items():
            #inventory['all']['children'][container_type] = {}
            inventory['all']['children'][container_type] = {}
            inventory['all']['children'][container_type]['hosts'] = []
            for container_name, container_ip_dict in container_dict.items():
                #inventory['all'][container_type][container_name] = None
                inventory['all']['children'][container_type]['hosts'].append(container_name)
        #print(json.dumps(inventory, indent=4, sort_keys=True))
        print(yaml.dump(inventory, default_flow_style=False)) 
    except yaml.YAMLError as e:
        print(e)
            
        
