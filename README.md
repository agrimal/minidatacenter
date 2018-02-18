# MiniDataCenter Project

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

The host must have 2 bridges called 'br-int' and 'br-ext'

Install Guide
=============

Clone this repository :

    git clone https://github.com/agrimal/minidatacenter.git /opt/minidc

Launch the executable :

    /opt/minidc/scripts/bootstrap-minidc.sh

Modify the config.yml file accordingly to your needs
* The container_interface's name can't include the '-' character
* The networks names must be the same in the 'networks' and 'containers' sections.

Create the containers :

    /opt/minidc/scripts/create-containers.py
