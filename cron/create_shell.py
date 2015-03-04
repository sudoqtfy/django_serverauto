#!/usr/bin/env python

import time
import os
import os.path as op
import re


cmd = '''
        rrdtool create {filepath} \\
        --step {step} \\
        --start {starttime} \\
        {dss} \\
        RRA:AVERAGE:0.5:1:600 \\
        RRA:AVERAGE:0.5:6:700 \\
        RRA:AVERAGE:0.5:24:775 \\
        RRA:AVERAGE:0.5:288:797 \\
        RRA:MIN:0.5:1:600 \\
        RRA:MIN:0.5:6:700 \\
        RRA:MIN:0.5:24:775 \\
        RRA:MIN:0.5:444:797 \\
        RRA:MAX:0.5:1:600 \\
        RRA:MAX:0.5:6:700 \\
        RRA:MAX:0.5:24:775 \\
        RRA:MAX:0.5:444:797 \\
'''

def create(filepath, *ds, **kw):
    global cmd

    params = dict(filepath=filepath)
    defaults = dict(
            step      = 300,
            starttime = str(int(time.time())),
            heartbeat = "600",
            dst       = 'GAUGE',
        )
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    if len(ds) == 0:
        logging.warning('DS is empty')
        return None
    ds_temp = ["DS:%s:%s:%s:0:U" % (dsname, params.get('dst', 'GAUGE'), params.get('heartbeat', '600'))  for dsname in ds]
    dss = ' \\\n\t'.join(ds_temp)
    params.setdefault('dss', dss)
    cmd2 = cmd.format(**params)
    os.system(cmd2)


def walk_create(filepath):
    print filepath
    fp = op.dirname(filepath)
    if not op.isdir(fp):
        os.makedirs(fp)
    if re.search('memory', op.basename(filepath)):
        create(filepath, 'free', 'usage')
    elif re.search('load', op.basename(filepath)):
        create(filepath, 'load01', 'load05', 'load15')
    elif re.search('traffic', op.basename(filepath)):
        create(filepath, 'out', 'in')


if __name__ == '__main__':
#    create('test.rrd', 'ds')
    walk_create('/tmp/memory1.rrd')
