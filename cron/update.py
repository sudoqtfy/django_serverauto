#!/usr/bin/env python

from snmp import get_snmp_data
import os
import rrdtool
import sys
import os.path as op
import time
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
        print 'connect mysql error'
        sys.exit()
    cursor.execute('select * from server_list')
    for server_list  in cursor.fetchall():
        ips.append(server_list[1])
    return ips



if __name__ == '__main__':
    while 1:
        ips = get_ip_list(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        d = get_snmp_data(ips)
        for k, v in d.items():
            if v is None:
                print '%s down' % k
                continue
            MemUsage =  v.get('MemUsage', 0)
            MemFree =  v.get('MemFree', 0)
            rra_file = op.join(rra_path, k+'/memory.rrd')
            if not op.isfile(rra_file):
                print '%s no found!' % rra_file
                continue
            cmd = 'rrdtool update %s N:%s:%s' % (rra_file, MemFree, MemUsage)
            os.system(cmd)
#            print rrdtool.updatev(rra_file, 'N:%s:%s' %(MemFree, MemUsage))
        time.sleep(300)

