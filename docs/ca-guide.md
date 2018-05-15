# The MiniDataCenter Project

## Certificate Authority Guide

### Description

**From the Certificate Authority page on [Wikipedia](https://en.wikipedia.org/wiki/Certificate_authority) :**

A certificate authority or certification authority (CA) is an entity that issues digital certificates.

A digital certificate certifies the ownership of a public key by the named subject of the certificate. This allows others (relying parties) to rely upon signatures or on assertions made about the private key that corresponds to the certified public key. A CA acts as a trusted third party—trusted both by the subject (owner) of the certificate and by the party relying upon the certificate. The format of these certificates is specified by the X.509 standard.

**From the Easy-RSA repository on [Github](https://github.com/OpenVPN/easy-rsa) :**

Easy-RSA is a CLI utility to build and manage a PKI CA.

In laymen's terms, this means to create a root certificate authority, and request and sign certificates, including sub-CAs and certificate revocation lists (CRL).

### Configuration

Example :
```yaml
all:
    children:
        containers:
            children:
                ca:
                    hosts:
                        ca-container:
                            network:
                                ethernets:
                                    ethint:
                                        addresses: [10.0.0.100/24]
                                    ethext:
                                        addresses: [192.168.0.100/24]
                                        gateway4: 192.168.0.1
                                        routes:
                                        - to: 0.0.0.0/0
                                          via: 192.168.0.1
                                        nameservers:
                                            addresses: [192.168.0.101, 192.168.0.1]
                            ansible_host: 10.0.0.100
                            ca_organisation: My_Organisation
                            ca_ou: my-domain.com
                            ca_country: FR
                            ca_province: Ile-de-France
                            ca_city: Paris
                            ca_email: admin@my-domain.com
                            ca_easy_rsa_install_dir: /etc/easy-rsa
                            ca_key_size: '2048'
                            ca_ca_expire: '1825'
                            ca_key_expire: '1825'
                            ca_certificates:
                                servers:
                                - vpn.my-domain.com
                                - ldap.my-domain.private
                                - lam.my-domain.com
                                clients:
                                - my_smartphone
                                - my_laptop01
                                - my_laptop02
                            renew_all_secrets: false
                            push_data_from_minidc_working_directory: false
```

### Details

**ca_organisation:** `string`

   Name of your organisation.

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

### Usage

**Alias :** `deploy_ca`

**Name of the playbook :** setup-ca.yml
