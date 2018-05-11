# The MiniDataCenter Project
## OpenLDAP 

Description
===========

From the official website : [www.openldap.org](https://www.openldap.org/)

OpenLDAP Software is an open source implementation of the Lightweight Directory
Access Protocol.

The suite includes:
- slapd - stand-alone LDAP daemon (server)
- libraries implementing the LDAP protocol, and
- utilities, tools, and sample clients.

Configuration
=============

Example :
```yaml
                ldap-container:
                    network:
                        ethernets:
                            ethint:
                                addresses: [10.0.0.7/24]
                            ethext:
                                addresses: [192.168.0.7/24]
                                gateway4: 192.168.0.1
                                routes:
                                - to: 0.0.0.0/0
                                  via: 192.168.0.1
                                nameservers:
                                    addresses: [192.168.0.2, 192.168.0.1]
                    ansible_host: 10.0.0.7
                    ca_pair: ca-container
                    ldap_certificate: ldap.example.private
                    ldap_organization: example.com
                    ldap_domain: example.com
                    ldap_listen_ips:
                    - 127.0.0.1
                    - 10.0.0.7
                    push_config: false
```

Details
=======

ca_pair: <string>
    Name of the container providing certificates.

lam_certificate: <string>
    Name of the certificate. Must be declared too in the "ca_certificates"
  section of the CA container.

ldap_organization: <string>
    Name of the organization to use in the base DN of your LDAP directory.

ldap_domain: <string>
    The DNS domain name is used to construct the base DN of the LDAP directory.
For example, 'foo.example.org' will create the directory with
'dc=foo, dc=example, dc=org' as base DN.

ldap_listen_ips: [<string>, …]
    Specify slapd's listening IP addresses.

push_config: <boolean>
    If true, the config files will be copied from localhost to the container.
  This is usefull if you want to restore a backup. If the files don't exist on
  localhost, this variable is considered false.
    If false, the config files will be copied from the container to localhost.
  This is usefull if you want to save your configuration.
    The directory used to store the files on localhost is the one declared in the
  'minidc_working_directory' variable.
