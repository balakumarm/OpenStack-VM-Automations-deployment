#!/usr/bin/env  python
import os
from novaclient import client

def get_creds():
    d = {}
    d['username'] = ''
    d['api_key'] = ''
    d['auth_url'] = ''
    d['project_id'] = ''
    return d

'''creds = get_creds()
nova = client.Client("2", **creds)
I = nova.servers.list()
print I '''
