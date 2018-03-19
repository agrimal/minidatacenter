alias deploy_all="/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-everything.yml"
alias deploy_localhost='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-localhost.yml'

alias deploy_common='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-common.yml'
alias deploy_ca='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-ca.yml'
alias deploy_dns='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-dns.yml'
alias deploy_dhcp='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-dhcp.yml'
alias deploy_rvprx='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-rvprx.yml'
alias deploy_vpn='/opt/minidc/python-venv/bin/ansible-playbook -i /opt/minidc/inventory.yml /opt/minidc/playbooks/setup-vpn.yml'
