#!/bin/bash
#
# MiniDataCenter Project
# Copyright 2018 Aurélien Grimal
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Packages needed for ldap-python :
# apt install gcc python3-dev libdpkg-perl libldap2-dev libsasl2-dev 

# The parent directory of this script
DIR="$(cd "$(dirname "$0")/.."; pwd)"

# Packages version
ANSIBLE_VERSION="2.6.8"
NETADDR_VERSION="0.7.19"
DNSPYTHON_VERSION="1.15.0"
PYTHON_LDAP_VERSION="3.1.0"

# Install package virtualenv if not already installed
dpkg-query -W -f='${Status}' virtualenv | grep 'ok installed' > /dev/null 2>&1

if ! dpkg -s virtualenv >/dev/null 2>&1; then
    echo "Installing package virtualenv..."
    apt install -y virtualenv
fi

if ! dpkg -s gcc >/dev/null 2>&1; then
    echo "Installing package virtualenv..."
    apt install -y gcc
fi

# Create a new virtualenv
rm -rf ${DIR}/python-venv
virtualenv -p python3 --clear ${DIR}/venv-python3

# Enter the virtualenv
source ${DIR}/venv-python3/bin/activate

# Install required python packages
# - netaddr required for ipaddr filter
pip install \
    ansible==$ANSIBLE_VERSION \
    netaddr==$NETADDR_VERSION \
    dnspython==$DNSPYTHON_VERSION \

