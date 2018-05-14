# The MiniDataCenter Project
## Domain Name System Guide

### Description

**From the Domain Name System page on [Wikipedia](https://en.wikipedia.org/wiki/Domain_Name_System) :**

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
                            - dhcp-container
                            renew_all_secrets: false
```

### Details

**dns_master_zones:** `{ forward : [{fwd_zone_1}, {fwd_zone_2}, …], reverse : [{rvs_zone_1}, {rvs_zone_2}, …] }`

* **forward:** `list of dictionaries` Each dictionary is a forward DNS zone  with the following keys :
  * **name:** `string` Name of the zone.  
              (ex : my-domain.com)  
    **ns_a_record:** `string` FQDN of this server in this zone, without the last dot, for the NS record.  
                     (ex : dns.my-domain.com)  
    **ns_ip:** `string` IP address of this server in this zone, for the NS record.  
               (ex : 192.168.1.5)  
    **ns_contact:** `string` First part of the email address (before the @) of the contact for this zone.  
                    (ex : admin).  
    **a_records:** `[[string, string], …]` List of each A record in this zone. each record is a list of 2 strings.  
                   The first string is the domain name, without the zone (ex : my-server).  
                   The second string is the IP address (ex : 192.168.1.10).  
    **txt_records:** `[[string, string], …]` List of each TXT record in this zone. Each record is a list of 2 strings.  
                     The first string is the domain name, without the zone (ex : my-server).  
                     The second string is the double-quoted text value (ex : '"This is a good server"').  
    **cname_records:** `[[string, string], …]` List of each CNAME record in this zone. Each record is a list of 2 strings.  
                       The first string is the alias (ex : service).  
                       The second string is the domain name, without the zone (ex : my-server).  
* **reverse:** `list of dictionaries` Each dictionary is a reverse DNS zone  with the following keys :
  * **subnet:** `string` Subnet of the zone in CIDR notation.  
                (ex : 192.168.1.0/24)  
    **ns_url:** `string` FQDN of this server in this zone, without the last dot, for the NS record.  
                (ex : dns.my-domain.com)  
    **ns_contact:** `string` First part of the email address (before the @) of the contact for this zone.  
                    (ex : admin).  
    **ptr_records:** `[[string, string], …]` List of each PTR record in this zone. each record is a list of 2 strings.  
                     The first string is the FQDN, without the last dot (ex : my-server.my-domain.com).  
                     The second string is the IP address (ex : 192.168.1.10).  

**dns_clients:** `[{ string : string }, …]` 

   List of dictionaries. Each dictionary is an ACL allowing to query the DNS server.
The first string is the name of the ACL, in fact it's just a comment in the configuration file) (ex : Clients).
The second string is the CIDR subnet allowed to query the DNS (ex : 192.168.0.0/24).

**dns_admins:** `[{ string : string }, …]`

   List of dictionaries. Each dictionary is an ACL allowing to update the DNS server.
The first string is the name of the ACL, in fact it's just a comment in the configuration file) (ex : DHCP Container).
The second string is the CIDR subnet allowed to query the DNS (ex : 10.0.0.102/32).

**dhcp_pairs:** `[string, …]`

   List of strings.
   Each string is the name of a DHCP server paired with this DNS server.
   The DHCP leases given by the DHCP server will be verified and updated in the DNS server.

**renew_all_secrets:** `boolean`

   If you run the playbook with this parameter set to 'true', then all keys (TSIG) will be deleted and generated again.

### Usage

**Alias :** `deploy_dns`

**Name of the playbook :** setup-dns.yml
