#!/usr/bin/env python
import os
import sys
import argparse
import yaml
from novaclient import client as novaclient
from fabric.api import *
from NC_servercreate import server_create
from NC_credential import get_creds
# passing Nova Cred
creds = get_creds()
nova = novaclient.Client("2", **creds)

# Fab environemnt values 
# set the user to use for ssh
env.user = 'root'

# Global Variables
svr_value_new = None
sname = None

## Reading the Values from Yaml Config 
conf_yaml = open('auto_conf.yaml')
vvalue = yaml.load(conf_yaml)
conf_yaml.close()

# Reading the environment Value of Project 
environ = vvalue['environment']
sprefix = vvalue['servername_prefix']
Sversion = vvalue['version'] 
opkeyname = vvalue['openstack_keyname']
wcb_package = vvalue['package_wcb']
wcs_package = vvalue['package_wcb']
keyfile_path = str(vvalue['keyfile_path'])
conf_path = str(vvalue['conf_path'])
# servername Function

def servername(sprefix,svr_value_new,snum):
    sname1 = []
    snum = snum+1
    for tnum in range(1,snum) :
        snamett = (sprefix+svr_value_new)+str(tnum)
        sname1.append(snamett)
        tnum+1
    return sname1

    
# Deploy Function
def deploy(server_ip,srv_value_new,environ):
     print server_ip
     print srv_value_new
     print environ
     env.host_string = server_ip 
     env.connection_attempts = 4
     keyfile_path = str(vvalue['keyfile_path'])
     env.key_filename = keyfile_path
     print keyfile_path
#     env.user = 'root'
     # Add your orchestration 
     sudo("echo %s > /.svrtype" % (srv_value_new))
     local("scp -i %s %s/yumrepo.tar root@%s:/etc/yum.repos.d" % (keyfile_path,conf_path,server_ip))
     local("scp -i %s %s/build_info.txt root@%s:/var/webex/version" % (keyfile_path,conf_path,server_ip))
    
     sudo('yum update -y ;yum install puppet -y')
# wcbsrv is one server type  and wcssrv is another server type 

     if srv_value_new == 'wcbsrv':
         for pkg_wcb in wcb_package:
             sudo ('yum install %s -y' % pkg_wcb)
     elif srv_value_new == 'wcssrv':
         for pkg_wcs in wcs_package:
             sudo ('yum install %s -y' % pkg_wcs) 


# Command line avrg with optparse 
# Creating the VM by server function WCB or WCS or both with number of servers

def main(argv): 
    parser = argparse.ArgumentParser(usage='\n Example %prog -n 2 -d wcb wcs')
    parser.add_argument('-n','--num', help='option num', dest='ns', action='store',nargs=1, type=int, default=1)
    parser.add_argument('-d','--dep', help='option wcb wcs', dest='dep', action='store',nargs="*")
    
    global opts
    opts = parser.parse_args()
    
    print opts
    
    if len(sys.argv[1:]) == 0:
        parser.error('Example %prog -n 2 -d wcb wcs') 
        parser.print_help()
        sys.exit(1)
    svr_crev = opts.dep
    snum = opts.ns
    snum = snum[0]
   
    for i in svr_crev:
        svr_value = i
        Sname = []
        Sname = servername(sprefix,svr_value,snum)
        print Sname
        for j in Sname:
            IP = server_create( j, svr_value, nova, Sversion, opkeyname )
            IP = str(IP)
            if svr_value == 'wcs':
                srv_value_t = 'wcssrv'
                print "Deploying the %s server ....." % j
                deploy(IP,srv_value_t,environ )
            elif svr_value == 'wcb':
                srv_value_t = 'wcbsrv'
                print "Deploying the %s server ....." % j
                deploy(IP,srv_value_t,environ )
            else:
                print "Server type is not defined" 
                
            
            
if __name__=='__main__':
    main(sys.argv)

     
