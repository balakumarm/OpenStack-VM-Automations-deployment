import os
import time
from novaclient import client as novaclient
from NC_credential import get_creds
creds = get_creds()
nova = novaclient.Client("2", **creds)
"""''' if not nova.keypairs.findall(name="mykey"):
    with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
        nova.keypairs.create(name="mykey", public_key=fpubkey.read()) '''"""

def server_create(sname,stype,nova,version,keyname):
    image = nova.images.find(name="CentOS6.3_x86_64")
 
    if stype == 'wcs':
        flavor = nova.flavors.find(name="m1.large")
    else:
        flavor = nova.flavors.find(name="m1.medium")
    mdata = {}  # Setting  Meta Data 
    mdata['function']=stype
    mdata['version']=str(version)
    instance = nova.servers.create(name=sname, image=image, flavor=flavor, meta=mdata, key_name=keyname)
#   Validating the Build Status 
    status = instance.status
    if status == 'ERROR':
        return status
    elif status == ('BUILD' or 'ACTIVE'):  # If Status is Active Assigning Floating IP Add
        instance = nova.servers.get(instance.id)
        ipaddr = server_assign_floatip(instance, nova)
        return ipaddr
    else:
        msgerr = "Unknown State"
        return msgerr 

def server_assign_floatip(sname_created,nova):
    ip_list = nova.floating_ips.list()
    status1 = sname_created.status 
    while status1 == 'BUILD':
        sname_created = nova.servers.get(sname_created.id)
        status1 = sname_created.status
    instance = sname_created.id 
    for i in ip_list:
        if i.instance_id == instance:
           result = "Server already allocated Floating IP" 
           break
        elif i.instance_id == None:
            ipaddr = i.ip
            sname_created = nova.servers.get(sname_created.id)
            sname_created.add_floating_ip(ipaddr)
            result = ipaddr
            break
        else:
            result = "No Floating IP's"
    return result

def main():
    print  server_create(sname, stype, nova,version, keyname )
if __name__ == '__main__':
    main()

