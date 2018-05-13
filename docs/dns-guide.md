# The MiniDataCenter Project
## Domain Name System Guide

### Description

**From the Domain Name System page on [Wikipedia]
(https://en.wikipedia.org/wiki/Domain_Name_System) :**
---

The Domain Name System (DNS) is a hierarchical decentralized naming system for
computers, services, or other resources connected to the Internet or a private
network.

It associates various information with domain names assigned to each of the
participating entities. Most prominently, it translates more readily memorized
domain names to the numerical IP addresses needed for locating and identifying
computer services and devices with the underlying network protocols.

By providing a worldwide, distributed directory service, the Domain Name System
is an essential component of the functionality on the Internet, that has been in
use since 1985.

**From the Bind page on [Wikipedia](https://en.wikipedia.org/wiki/BIND) :**

BIND, or named, is the most widely used Domain Name System (DNS) software on the
Internet. On Unix-like operating systems it is the de facto standard.

### Configuration

Example :
```yaml
all:
    children:
        containers:
            children:
                dns:
                    hosts:
                        dns-container:
                            network:
                                ethernets:
                                    ethint:
                                        addresses: [10.0.0.101/24]
                                    ethext:
                                        addresses: [192.168.0.101/24]
                                        gateway4: 192.168.0.1
                                        routes:
                                        - to: 0.0.0.0/0
                                          via: 192.168.0.1
                                        nameservers:
                                            addresses: [127.0.0.1, 192.168.0.1]
                            ansible_host: 10.0.0.101
                            dns_master_zones:
                                forward:
                                - name: my-domain.com
                                  ns_a_record: dns.my-domain.com
                                  ns_ip: 192.168.0.101
                                  ns_contact: admin
                                  a_records:
                                  - [ca-container       , 192.168.0.100]
                                  - [dns-container      , 192.168.0.101]
                                  - [dhcp-container     , 192.168.0.102]
                                  - [rvprx-container    , 192.168.0.103]
                                  - [vpn-container      , 192.168.0.104]
                                  - [ldap-container     , 192.168.0.105]
                                  - [lam-container      , 192.168.0.106]
                                  - [cyrus-container    , 192.168.0.107]
                                  - [plex-container     , 192.168.0.108]
                                  - [mariadb-container  , 192.168.0.109]
                                  - [smtp-container     , 192.168.0.110]
                                  - [smb-container      , 192.168.0.111]
                                  - [nextcloud-container, 192.168.0.112]
                                  txt_records: []
                                  cname_records:
                                  - [vpn,  vpn-container]
                                  - [lam, lam-container]
                                  - [plex, plex-container]
                                - name: my-domain.home
                                  ns_a_record: dns.my-domain.home
                                  ns_ip: 192.168.0.101
                                  ns_contact: admin
                                  a_records: []
                                  txt_records: []
                                  cname_records: []
                                - name: my-domain.private
                                  ns_a_record: dns.my-domain.private
                                  ns_ip: 10.0.0.101
                                  ns_contact: admin
                                  a_records:
                                  - [ca-container       , 10.0.0.100]
                                  - [dns-container      , 10.0.0.101]
                                  - [dhcp-container     , 10.0.0.102]
                                  - [rvprx-container    , 10.0.0.103]
                                  - [vpn-container      , 10.0.0.104]
                                  - [ldap-container     , 10.0.0.105]
                                  - [lam-container      , 10.0.0.106]
                                  - [cyrus-container    , 10.0.0.107]
                                  - [plex-container     , 10.0.0.108]
                                  - [mariadb-container  , 10.0.0.109]
                                  - [smtp-container     , 10.0.0.110]
                                  - [smb-container      , 10.0.0.111]
                                  - [nextcloud-container, 10.0.0.112]
                                  txt_records: []
                                  cname_records:
                                  - [ldap, ldap-container]
                                reverse:
                                - subnet: 192.168.1.0/24
                                  ns_url: dns.my-domain.com
                                  ns_contact: admin
                                  ptr_records:
                                  - [ca-container.my-domain.com       , 192.168.0.100]
                                  - [dns-container.my-domain.com      , 192.168.0.101]
                                  - [dhcp-container.my-domain.com     , 192.168.0.102]
                                  - [rvprx-container.my-domain.com    , 192.168.0.103]
                                  - [vpn-container.my-domain.com      , 192.168.0.104]
                                  - [ldap-container.my-domain.com     , 192.168.0.105]
                                  - [lam-container.my-domain.com      , 192.168.0.106]
                                  - [cyrus-container.my-domain.com    , 192.168.0.107]
                                  - [plex-container.my-domain.com     , 192.168.0.108]
                                  - [mariadb-container.my-domain.com  , 192.168.0.109]
                                  - [smtp-container.my-domain.com     , 192.168.0.110]
                                  - [smb-container.my-domain.com      , 192.168.0.111]
                                  - [nextcloud-container.my-domain.com, 192.168.0.112]
                                - subnet: 10.0.0.0/24
                                  ns_url: dns.my-domain.private
                                  ns_contact: admin
                                  ptr_records:
                                  - [ca-container.my-domain.private       , 10.0.0.100]
                                  - [dns-container.my-domain.private      , 10.0.0.101]
                                  - [dhcp-container.my-domain.private     , 10.0.0.102]
                                  - [rvprx-container.my-domain.private    , 10.0.0.103]
                                  - [vpn-container.my-domain.private      , 10.0.0.104]
                                  - [ldap-container.my-domain.private     , 10.0.0.105]
                                  - [lam-container.my-domain.private      , 10.0.0.106]
                                  - [cyrus-container.my-domain.private    , 10.0.0.107]
                                  - [plex-container.my-domain.private     , 10.0.0.108]
                                  - [mariadb-container.my-domain.private  , 10.0.0.109]
                                  - [smtp-container.my-domain.private     , 10.0.0.110]
                                  - [smb-container.my-domain.private      , 10.0.0.111]
                                  - [nextcloud-container.my-domain.private, 10.0.0.112]
                            dns_clients:
                            - { Clients : 192.168.0.0/24 }
                            dns_admins:
                            - { DHCP container : 10.0.0.102/32 }
                            dhcp_pairs:
                            - ubudhcp01
                            renew_all_secrets: false
```

Details
=======

**dns_master_zones:** `{ forward : [], reverse : [] }`

   forward: list of all the forward zones this DNS will handle
  

**ca_ou:** `string`

   Name of your organizational unit.

**ca_country:** `string`

   Two-letter code (ISO 3166-1 alpha-2) of your country (cf. [Wikipedia](https://
en.wikipedia.org/wiki/ISO_3166-1_alpha-2))

**ca_province:** `string`
    
    Name of your province.

**ca_city:** `string`

    Name of your city.

**ca_email:** `string`

    Email of the administrator of the CA.

**ca_easy_rsa_install_dir:** `string`

    Directory where to install Easy-RSA.

**ca_key_size:** `integer`

    Size (in bits) of the keys.

**ca_ca_expire:** `integer`

    Number of days of CA key validity.

**ca_key_expire:** `integer`

    Number of days of certificates validity.

**ca_certificates:** `{ servers: [string, …], clients: [string, …] }`

    Names of the certificates that you want to generate.
Put in 'servers' the servers certificates and in 'clients' the clients
certificates.
When you delete a certificate from one list, it is revoked and added to the
Certificate Revokation List (CRL).

**renew_all_secrets:** `boolean`

    If you run the playbook with this parameter set to 'true', then all keys and
certificates (including the CA's ones) will be deleted and generated again.

**push_data_from_minidc_working_directory:** `boolean`

    If you run the playbook with this parameter set to 'true', then all the
directory containing the keys and the certificates will be copied from the host
to the container. This is useful if you want to restore a backup.

Usage
=====

**Alias :** `deploy_ca`

**Name of the playbook :** setup-ca.yml
