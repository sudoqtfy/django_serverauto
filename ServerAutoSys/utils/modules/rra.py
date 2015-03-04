#!/usr/bin/env python

from snmp import get_snmp_data
import rrdtool
import time
import os
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
cur_time = str(int(time.time()))
'''
ret = rrdtool.create('Traffic.rrd','--step','300','--start',cur_time,
        'DS:wlan0_in:COUNTER:600:0:U',
        'DS:wlan0_out:COUNTER:600:0:U',
        'RRA:AVERAGE:0.5:1:600',
	'RRA:AVERAGE:0.5:6:700',
	'RRA:AVERAGE:0.5:24:775',
	'RRA:AVERAGE:0.5:288:797',
	'RRA:MAX:0.5:1:600',
	'RRA:MAX:0.5:6:700',
	'RRA:MAX:0.5:24:775',
	'RRA:MAX:0.5:444:797',
	'RRA:MIN:0.5:1:600',
	'RRA:MIN:0.5:6:700',
	'RRA:MIN:0.5:24:775',
	'RRA:MIN:0.5:444:797')
'''
ips = ['127.0.0.1']
res = get_snmp_data(ips)
for k, v in res.items():
    if isinstance(v, dict):
        Traffic = v.get('Traffic', '')
        if Traffic:
            wlan0 = Traffic.get('wlan0', '')
            wlan0_out, wlan0_in = wlan0.split(':')
#            print wlan0_out, wlan0_in
            update = rrdtool.updatev(CUR_DIR+'/Traffic.rrd','%s:%s:%s' % (cur_time, wlan0_in, wlan0_out))
            print update
