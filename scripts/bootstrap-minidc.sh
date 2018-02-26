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

# The parent directory of this script
DIR="$(cd "$(dirname "$0")/.."; pwd)"

# Packages version
ANSIBLE_VERSION="2.4.3.0"
PYLXD_VERSION="2.2.4"
NETADDR_VERSION="0.7.19"
DNSPYTHON_VERSION="1.15.0"

# Install package virtualenv if not already installed
dpkg-query -W -f='${Status}' virtualenv | grep 'ok installed' > /dev/null 2>&1

if [ $? -eq 1 ]; then
    echo "Installing package virtualenv..."
    apt install -y virtualenv
fi

# Create a new virtualenv
rm -rf ${DIR}/python-venv
virtualenv -p python3 --clear ${DIR}/python-venv

# Enter the virtualenv
source ${DIR}/python-venv/bin/activate

# Install required python packages
pip install \ 
    ansible==$ANSIBLE_VERSION \
    pylxd==$PYLXD_VERSION \ 
    netaddr==$NETADDRVERSION \
    dnspython==$DNSPYTHON_VERSION

# Put correct shebang in python scripts
sed -i "s,%%SHEBANG%%,#!${DIR}/python-venv/bin/python," ${DIR}/scripts/create-containers.py
sed -i "s,%%SHEBANG%%,#!${DIR}/python-venv/bin/python," ${DIR}/scripts/inventory.py
