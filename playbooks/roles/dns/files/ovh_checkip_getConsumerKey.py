#!/usr/bin/env python3

import ovh

# create a client using configuration
client = ovh.Client()

# Request RO, /me API access
ck = client.new_consumer_key_request()
#ck.add_rules(ovh.API_READ_ONLY, "/me") # Read only
ck.add_recursive_rules(ovh.API_READ_WRITE, '/') # Read / Write

# Get ConsumerKey (CK)
validation = ck.request()

print("Please follow this link and authenticate :\n{}".format(validation['validationUrl']))
input("Once done, press a key to continue...")

# Print nice welcome message
print("Welcome", client.get('/me')['firstname'])
print("Your 'ConsumerKey' is '{}'".format(validation['consumerKey']))
