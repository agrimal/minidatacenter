# The MiniDataCenter Project
## LDAP Account Manager Guide

Description
===========

From the author website : [www.ldap-account-manager.org](https://www.ldap-account-manager.org/lamcms/)

LDAP Account Manager (LAM) is a webfrontend for managing entries (e.g. users, 
groups, DHCP settings) stored in an LDAP directory. LAM was designed to make LDAP
management as easy as possible for the user. It abstracts from the technical 
details of LDAP and allows persons without technical background to manage LDAP 
entries. If needed, power users may still directly edit LDAP entries via the 
integrated LDAP browser.

Configuration
=============

Example :
```yaml
all:
    children:
        containers:
            children:
                ldap:
                    hosts:
                        lam-container:
                            network:
                                ethernets:
                                    ethint:
                                        addresses: ['10.0.0.8/24']
                                    ethext:
                                        addresses: ['192.168.0.8/24']
                                        gateway4: '192.168.0.1'
                                        routes:
                                        - to: '0.0.0.0/0'
                                          via: '192.168.0.1'
                                        nameservers:
                                            addresses: ['192.168.0.2', '192.168.0.1']
                            ansible_host: '10.0.0.8'
                            ca_pair: ca-container
                            lam_certificate: lam.example.com
                            lam_url: lam.example.com
                            lam_admin_mail: admin@example.com
                            ldap_url: ldap.example.private
                            ldap_rootdn: 'dc=example,dc=com'
                            push_config: false
```

Details
=======

**ca_pair:** `string`

   Name of the container providing certificates.

**lam_certificate:** `string`

   Name of the certificate. Must be declared too in the "ca_certificates"
  section of the CA container.

**ldap_url:** `string`

   URL of LAM server.

**lam_admin_mail:** `string`
    Mail of the administrator

**push_config:** `boolean`
   If true, the config files will be copied from localhost to the container.
  This is usefull if you want to restore a backup. If the files don't exist on
  localhost, nothing is done.
  
   If false, the config files will be copied from the container to localhost.
  This is usefull if you want to save your configuration.
  
   The directory used to store the files on localhost is the one declared in the
  'minidc_working_directory' variable.

First Use
=========

- Enter the URL in your browser to access LAM (http://lam.example.com).
If everything works fine, you should be redirected to HTTPS this way :
https://lam.tech-tips.fr/lam/templates/login.php

- First you have to change the master password.
To do so, click on "LAM configuration" on the upper right corner, then on
"Edit general settings". The default password is 'lam'. Click "Ok". At the
bottom of the page, enter your new password.
This password is stored in the /etc/ldap-account-manager/config.cfg file.

- Then you have to configure the "lam" profile.
To do so, get back on the LAM home page, click on "LAM configuration" on the
upper right corner, then on "Edit server profiles". Again, the default password
is 'lam'. Click "Ok".

Example minimum config :

### "General Settings" tab :

- Server settings
Server address : ldap://ldap.example.private:389
Activate TLS : yes
Tree suffix : dc=example,dc=com
LDAP search limit : -

- Security settings
Login method : Fixed list
List of valid users : cn=admin,dc=example,dc=com

- Profile password : change the default password

### "Account types" tab :

- Users
LDAP Suffix : ou=people,dc=tech-tips,dc=fr
List attributes : leave default values
Custom label : leave empty
Additional LDAP filter : leave empty
Hidden : leave unchecked

- Groups
LDAP Suffix : ou=group,dc=tech-tips,dc=fr
List attributes : leave default values
Custom label : leave empty
Additional LDAP filter : leave empty
Hidden : leave unchecked

- Add a new "Applications" section by clicking the green cross on the Users line
LDAP Suffix : ou=applications,dc=tech-tips,dc=fr
List attributes : #uid;#cn;
Custom label : Applications
Additional LDAP filter : leave empty
Hidden : leave unchecked

### "Modules" tab :

- Users : Personal (inetOrgPerson), Unix (posixAccount), Shadow (shadowAccount)
- Groups : Unix (posixGroup)
- Applications : Account (account), Unix (posixAccount), Shadow (shadowAccount)

### "Module settings" tab :

- In the first "Unix" section :
Change "Password hash type" from "SSHA" to "CRYPT-SHA512"
Click "Advanced options" and change "User name suggestion" from "@givenname@%sn%"
to "%givenname%.%sn%"

Now click on the save button, go back on the profile configuration page, log in
with your new password, and verify every parameter again.

ENJOY
=====

Now you can start using LAM.

- Go to the home LAM page, and log in with "admin/password" credentials.
- On the first login, LAM detects that OU are missing and propose to create them :

```
The following suffixes are missing in LDAP. LAM can create them for you.
You can setup the LDAP suffixes for all account types in your LAM server profile
on tab "Account types".
ou=people,dc=example,dc=com
ou=group,dc=example,dc=com
ou=applications,dc=example,dc=com
```

- Click "Create"

- Change admin password :
  - Click on the "Tree View" button on the upper right corner.
  - Under dc=example,dc=com, click on "cn=admin".
  - In the "userPassword" section, enter your password, change "ssha" to
"crypt-sha512" and click "Update object"

- Create groups, users, applicative accounts, modify LAM to what you need.
