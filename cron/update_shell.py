#!/usr/bin/env python

from snmp import get_snmp_data
import os
#import rrdtool
import sys
import os.path as op
import time
from create_shell import walk_create
rra_path = '/data/django_serverauto/ServerAutoSys/rra'
DB_HOST = '127.0.0.1'
DB_NAME =  'ServerAutoSys'
DB_USER = 'root'
DB_PASS = 'root'

def get_ip_list(DB_HOST, DB_USER, DB_PASS, DB_NAME):
    import MySQLdb
    ips = []
    try:
        conn = MySQLdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        cursor = conn.cursor()
    except Exception,e:
        print 'connect mysql error:%s' % e
        sys.exit()
    cursor.execute('select * from server_list where server_snmp_on=1')
    for server_list  in cursor.fetchall():
        ips.append(server_list[1])
    return ips



if __name__ == '__main__':
    ips = get_ip_list(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    d = get_snmp_data(ips)
    for k, v in d.items():
        if v is None:
            print '%s down' % k
            continue
        ### memory update
        MemUsage =  v.get('MemUsage', 0)
        MemFree =  v.get('MemFree', 0)
        rra_file = op.join(rra_path, k+'/memory.rrd')
        if not op.isfile(rra_file):
            print '%s no found! creating...' % rra_file
            walk_create(rra_file)
        cmd = 'rrdtool update %s N:%s:%s' % (rra_file, MemFree, MemUsage)
        os.system(cmd)
        ### load update
        load01, load05, load15 = v.get('LoadAvg').split()
        rra_file = op.join(rra_path, k+'/loadavg.rrd')
        if not op.isfile(rra_file):
            print '%s no found! creating...' % rra_file
            walk_create(rra_file)
        cmd = 'rrdtool update %s N:%s:%s:%s' % (rra_file, load01, load05, load15)
        os.system(cmd)
        ### traffic
        traffic = v.get('Traffic')
        if isinstance(traffic, dict):
            for ifcname, ifcdata in traffic.items():
                rrdname = 'traffic_%s.rrd' % ifcname
                rra_file = op.join(rra_path, k+'/%s') % rrdname
                outs, ins = ifcdata.split(':')
                if not op.isfile(rra_file):
                    print '%s no found! creating...' % rra_file
                    walk_create(rra_file)
                cmd = 'rrdtool update %s N:%s:%s' % (rra_file, outs, ins)
                os.system(cmd)

#            print rrdtool.updatev(rra_file, 'N:%s:%s' %(MemFree, MemUsage))
