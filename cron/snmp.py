#!/usr/bin/env python
from IPy import IP
import netsnmp
import json
import sys
import subprocess
import traceback
import Queue
import multiprocessing
import time
class Snmp(object):
    
    def __init__(self,
            oid='.1.3.6.1.4.1.2021.8.1.101',
            DestHost='127.0.0.1',
            Version=2,
            Community='public'):
        self.oid = oid
        self.DestHost = DestHost
        self.Version = Version
        self.Community = Community


    def query(self):
        result = None 
        try:
            result = netsnmp.snmpwalk(
                    self.oid,
                    DestHost = self.DestHost,
                    Version = self.Version,
                    Community = self.Community)
        except Exception, e:
            print e
        finally:
            return result



def ping(host):
    
    cmd = 'ping -c 1 %s' % host
    ret = subprocess.call(cmd,
            shell  = True,
            stdout = open('/dev/null','w'),
            stderr = subprocess.STDOUT)
    if ret == 0:
        return True
    else:
        return False


def snmp_query(host_queue, result_dict):
    try:
        while not host_queue.empty():
            host = host_queue.get(block=False)
            if not ping(host): result_dict.setdefault(host, None)
            s = Snmp(DestHost=host)
            res = s.query()
            res = res[0] if len(res) != 0 else None
            result_dict.setdefault(host, res)
    except Queue.Empty:
        pass
    except:
        traceback.print_exc()

    
#ips = IP('192.168.1.0/24')
#for i in range(len(ips)):
#    iq.put(ips[i])
def get_snmp_data(ips):
    manage = multiprocessing.Manager()
    host_queue = manage.Queue()
    result_dict = manage.dict()
    workers = []
    try:
        for i in range(len(ips)):
            host_queue.put(ips[i])
    finally:
    
        for i in range(len(ips)):
            prc = multiprocessing.Process(
                    target = snmp_query,
                    args = (host_queue, result_dict)
                    )
            prc.start()
            workers.append(prc)
    
    
    for worker in workers:
        worker.join()
    
    for k, v in result_dict.items():
        if v is not None and isinstance(v, str):
            result_dict[k] = eval(v)
    return result_dict
if __name__ == '__main__':
    ips = ['192.168.56.2']
    print get_snmp_data(ips)
    #s = Snmp()
    #d = s.query()[0]
    #print d
