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

# Where to store the MiniDC files
MINIDC_DIR="/opt/minidc"

# Packages version
ANSIBLE_VERSION="2.4.3.0"
PYLXD_VERSION="2.2.4"

# MiniDataCenter git repo
MINIDC_GIT_REPO="https://github.com/agrimal/minidatacenter.git"

# Install package virtualenv if not already installed
dpkg-query -W -f='${Status}' virtualenv | grep 'ok installed' > /dev/null 2>&1

if [ $? -eq 1 ]; then
    echo "Installing package virtualenv..."
    apt install -y virtualenv
fi

# Create new virtualenv
rm -rf ${MINIDC_DIR}/python-venv
virtualenv -p python3 --clear ${MINIDC_DIR}/python-venv

source ${MINIDC_DIR}/python-venv/bin/activate

pip install ansible==$ANSIBLE_VERSION pylxd==$PYLXD_VERSION

git clone $MINIDC_GIT_REPO ${MINIDC_DIR}/minidc

DIR="$(dirname "${0}")/.."
echo "'$DIR'"

sed -i "s,%%SHEBANG%%,${DIR}/bin/python," ${DIR}/scripts/create-containers.py
