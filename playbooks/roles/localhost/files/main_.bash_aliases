alias deploy_all="/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/scripts/inventory.py /opt/minidc/playbooks/setup-everything.yml"
alias deploy_localhost='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-localhost.yml'
alias deploy_ca='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/scripts/inventory.py /opt/minidc/playbooks/setup-ca.yml'
alias deploy_dns='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/scripts/inventory.py /opt/minidc/playbooks/setup-dns.yml'
alias deploy_dhcp='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/scripts/inventory.py /opt/minidc/playbooks/setup-dhcp.yml'
