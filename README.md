# The MiniDataCenter Project

Description
===========

At the time of cloud-based infrastructure, where your personal and private
data could be compromised, The MiniDataCenter Project is a solution allowing you
to bring back your data at home. Moreover, it will let your discover all the
mecanisms lying under all the internet services you are using everyday.

What your need is just a single physical computer, connected to the internet
via your ISP router. This program will then deploy several preconfigured LXD
containers, using Ansible, an automation tool, with the following roles :

Implemented :
- [x] Certificate Authority
- [x] DNS Server

Coming soon :
- [ ] DHCP Server
- [ ] VPN Server
- [ ] Reverse Proxy Server
- [ ] LDAP Server
- [ ] LAM (LDAP Account Manager) Server
- [ ] Cyrus Server (mail)
- [ ] SMTP Relay Server

Quick Install Guide
===================

1. Install your computer / server following this guide :
[Host Install Guide](docs/host_install_guide.md)

2. Clone this repository :

```bash
git clone https://github.com/agrimal/minidatacenter.git /opt/minidc
```

3. Bootstrap the MiniDataCenter :

```bash
/opt/minidc/scripts/bootstrap-minidc.sh
```

4. Modify the config.yml file accordingly to your needs

5. Create the containers :

```bash
/opt/minidc/scripts/create-containers.py
```

6. Launch the Ansible playbook :

```bash
/opt/minidc/python-venv/bin/ansible-playbook \ 
    -i /opt/minidc/scripts/inventory.py \ 
    /opt/minidc/playbooks/setup-everything.yml
```

7. Enjoy !

License
=======

 The MiniDataCenter Project
 Copyright 2018 Aurélien Grimal

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
