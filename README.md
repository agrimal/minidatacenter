# The MiniDataCenter Project


License
=======

 Copyright (c) 2018 Aurélien Grimal

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

Description
===========

The MiniDataCenter Project is a solution that allow you to deploy at home,
on a single physical server, several LXD containers with the following roles :
* DNS Server
* DHCP Server
* VPN Server
* RVPRX (Reverse Proxy) Server
* LDAP Server
* LAM (LDAP Account Manager) Server
* Cyrus Server (mail)
* SMTP Relay Server

Prerequisites
=============

The host must :
* have a full internet access and not be behind a proxy.

Install Guide
=============

Clone this repository :

    git clone https://github.com/agrimal/minidatacenter.git /opt/minidc

Bootstrap the MiniDataCenter :

    /opt/minidc/scripts/bootstrap-minidc.sh

Modify the config.yml file accordingly to your needs

Create the containers :

    /opt/minidc/scripts/create-containers.py

Launch the Ansible playbook :

    /opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/scripts/inventory.py /opt/minidc/playbooks/setup-everything.yml
