#!/usr/bin/env python

import rrdtool
import time
import sys
import string
import random
import logging
import os
import re
import os.path as op
import fnmatch



def create(filename, *ds, **kw):
    '''
        create('memory1.rrd, 'free', 'usage')
    '''
    params = dict(filename=filename, ds=ds)
    defaults = dict(step="300", start=str(int(time.time())),heartbeat="600")
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    ds = params.get('ds', [])
    if len(ds) == 0:
        logging.warning('DS is empty')
        return None
    ds_temp = ["DS:%s:GAUGE:%s:0:U" % (dsname, params.get('heartbeat', '600'))  for dsname in ds]
    ret = rrdtool.create(
            params.get('filename', 'default.rrd'),
            "--step", params.get('step', "300"),
            "--start", params.get('start', str(int(time.time()))),
            ds_temp,
            "RRA:AVERAGE:0.5:1:600",
            "RRA:AVERAGE:0.5:6:700",
            "RRA:AVERAGE:0.5:24:775",
            "RRA:AVERAGE:0.5:288:797",
            "RRA:MIN:0.5:1:600",
            "RRA:MIN:0.5:6:700",
            "RRA:MIN:0.5:24:775",
            "RRA:MIN:0.5:444:797",
            "RRA:MAX:0.5:1:600",
            "RRA:MAX:0.5:6:700",
            "RRA:MAX:0.5:24:775",
            "RRA:MAX:0.5:444:797",
        )
    if ret is None:
        return ds
    else:
        logging.error('rrdtool create method error!')
        return None


def update(filename, *ds):
    ret = rrdtool.updatev(filename, 'N:%s' % (':'.join(ds)))
    print ret


def graph(rrdfile,destdir, *ds, **kw):
    '''
    graph('memory1.rrd', 'usage', 'free', title='memory usage', legendprefix='memory')
    '''
    colors = lambda: ''.join([random.choice(string.digits+'ABCDEF') for i in range(6)])
    params = dict(rrdfile=rrdfile, ds=ds, destdir=destdir)
    defaults = dict(start='-1d', width="750", height="260", title='default graph', legendprefix='legend', X=None)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)

    def_list = ["DEF:%s=%s:%s:AVERAGE" % (dsname, params.get('rrdfile'), dsname) for dsname in params.get('ds')]
    print params.get('rrdfile')
    png_file = op.basename(params.get('rrdfile')).rsplit('.')[0] + '.png'
    print png_file
    vdef = ["VDEF:{0}avg={0},AVERAGE",
            "VDEF:{0}max={0},MAXIMUM",
            "VDEF:{0}min={0},MINIMUM",
            "VDEF:{0}last={0},LAST"]

    graph_string = "AREA:{0}#{1}:{2} {0}"
    gprint_choice1 = [ 
                "GPRINT:{0}last:%6.2lf %Sbps",
                "GPRINT:{0}max:%6.2lf %Sbps",
                "GPRINT:{0}min:%6.2lf %Sbps",
                "GPRINT:{0}avg:%6.2lf %Sbps\l"]

    gprint_choice2 = [ 
                "GPRINT:{0}last:%6.2lf",
                "GPRINT:{0}max:%6.2lf",
                "GPRINT:{0}min:%6.2lf",
                "GPRINT:{0}avg:%6.2lf\l"]
    X = params.get('X')
    x_list = [] 
    if X is not None:
        x_list = ['-X', str(X)]
    gprint = gprint_choice1 if X is None else gprint_choice2
    vdef_list = []
    gprint_list = []
    for dsname in params.get('ds'):
        for vdef_string in vdef:
            vdef_string = vdef_string.format(dsname)
            vdef_list.append(vdef_string)
        graph_string_temp = graph_string.format(dsname, colors(), params.get('legendprefix', 'legend'))
        gprint_list.append(graph_string_temp)
        for gprint_string in gprint:
            gprint_string = gprint_string.format(dsname)
            gprint_list.append(gprint_string)
    print op.join(params.get('destdir'), png_file)
    rrdtool.graph(
            op.join(params.get('destdir'), png_file),
            #png_file,
            "--start", params.get('start', '-1d'),
            #"--vertical-label=memory",
            "--title", params.get('title', 'default'), "--width", params.get('width', "750"), "--height", params.get('height', "260"), "--x-grid", "MINUTE:12:HOUR:1:HOUR:1:0:%H",
            '-Y',
            x_list,
            def_list,
            vdef_list,
            "COMMENT:\\r",
            "COMMENT:\t\t ",
            "COMMENT:Last        ",
            "COMMENT:Maximum     ",
            "COMMENT:Minimum     ",
            "COMMENT:Average \l",
            gprint_list,
            "COMMENT:\\r",
            #"HRULE:4294967296#FF0000:Alarm value",
            #"GPRINT:total:AVERAGE:Total memory\:%6.2lf %Sbps\l",
            "COMMENT:\\r",
            "COMMENT:%sLast update\: %s" % ('\t'*14, time.strftime('%Y-%m-%d  %H\:%M\:%S')),
        )



def walk_graph(rrapath, destdir,):
    if not op.isdir(destdir):
        os.makedirs(destdir)
    for root, dirs, files in os.walk(rrapath):
        if len(files) == 0:
            sys.exit()
        for filename in files:
            if not fnmatch.fnmatch(filename, '*.rrd'): continue
            file_path = op.join(root, filename)
#            print file_path, destdir
            if re.search('memory', filename):
                graph(file_path, destdir, 'usage', 'free', title='memory usage', legendprefix='memory')



if __name__ == '__main__':
#   create('memory1.rrd', 'free', 'usage')
#   graph('/data/django_serverauto/ServerAutoSys/rra/127.0.0.1/memory1.rrd', '/data/django_serverauto/ServerAutoSys/static/rra/127.0.0.1','usage', 'free', title='memory usage', legendprefix='memory')
    graph('memory1.rrd', 'usage', 'free')
#    update('memory1.rrd' ,'60000000', '50000000')
#    walk_graph('/data/django_serverauto/ServerAutoSys/rra/127.0.0.1', '/data/django_serverauto/ServerAutoSys/static/rra/127.0.0.1')
