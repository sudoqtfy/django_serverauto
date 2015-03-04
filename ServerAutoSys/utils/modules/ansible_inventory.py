#!/usr/bin/env python

import os
import sys
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
activate_this = '/data/django_serverauto/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
try:
    import json
except ImportError:
    import simplejson as json

import argparse
sys.path.append(os.path.dirname(CUR_PATH))
from config import LOG_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from app.models import *


class Server2inventory():

    
    def __init__(self):
        self.inventory = {}
        self.parse_cli_args()
        self._getServerList(ServerGroup, ServerList)
        if self.args.list:
            data_to_print = json.dumps(self.inventory, indent=4)
        elif self.args.host:
            data_to_print = get_host_info(ServerList, self.args.host.hostname)
        print data_to_print



    def get_host_info(self, models, hostname):
        try:
            obj = models.objects.get(server_name=hostname)
            host = {'ansible_ssh_host': obj.server_ip}
            port = {'ansible_ssh_port': server_port}
            d = dict(host.items()+port.items())
        except:
            return None
        return json.dumps(d)
        

    def _getServerList(self, group_model, child_model):
        groups = group_model.objects.all() 
        if len(groups) == 0: return False
        for group in groups:
            child_objs = child_model.objects.filter(server_groupname=group)
            if len(child_objs) == 0: continue
            self.inventory.setdefault(group.server_groupname, [])
            l = []
            for obj in child_objs:
                user = obj.server_user
                port = obj.server_port
                passwd = obj.server_pass
                ip = obj.server_ip
                host = obj.server_name
                host_d = {'ansible_ssh_host': ip}
#                d = dict(host_d.items())
                d = dict(ansible_ssh_host=ip, ansible_ssh_port=port)
                l.append("%s:%s" % (ip, port))
                str = '{1}:{2}'.format(user, ip, port)
                self.inventory[group.server_groupname].append(json.dumps(d))


    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on EC2')
        parser.add_argument('--list', action='store_true', default=True,
                           help='List instances (default: True)')
        parser.add_argument('--host', action='store',dest='hostname',
                           help='Get all the variables about a specific instance')
#        parser.add_argument('--refresh-cache', action='store_true', default=False,
#                           help='Force refresh of cache by making API requests to EC2 (default: False - use cache files)')
        self.args = parser.parse_args()



Server2inventory()
