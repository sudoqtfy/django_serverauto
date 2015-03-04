#!/usr/bin/env python

import time
import os
import os.path as op
import fnmatch
import random
import string
import re

cmd = '''
        rrdtool \\
        graph \\
        {filepath} \\
        --start  {starttime}\\
        --end {endtime}\\
        --vertical-label="{vertical}" \\
        --title "{title}" \\
        --width {width}  --height {height} \\
        --x-grid  MINUTE:12:HOUR:1:HOUR:1:0:%H \\
        -Y \\
        -X \\
        {X} \\
        {defs} \\
        {vdefs} \\
        COMMENT:"\\r" \\
        COMMENT:"{comtabs}"  \\
        COMMENT:"Last      " \\
        COMMENT:"Maximum   " \\
        COMMENT:"Minimum   " \\
        COMMENT:"Average \l" \\
        {gprints} \\
        COMMENT:"\\r"\\
        COMMENT:"{lasttimetabs}Last update\: {lasttime}" \\
'''
#        GPRINT:alarm:"%6.2lf %Sbps\l"\\
#        HRULE:4214#FF0000:"Alarm Line\l" \\
#        COMMENT:"\\r" \\




def graph(rrdfile, *ds, **kw):
    global cmd
    colors = lambda: ''.join([random.choice(string.digits+'ABCDEF') for i in range(6)])
    params = dict(
            rrdfile = rrdfile,
            
        )
    defaults = dict(
            vertical     = '',
            starttime    = '-1d',
            endtime      = 'now',
            width        = "750",
            height       = "260",
            title        = 'default graph',
            filepath     = 'default_{0}.png'.format(str(time.strftime('%Y_%m_%d_%H_%M_%S'))),
            legendprefix = 'legend',
            X            = 9,
            lasttime     = str(time.strftime('%Y-%m-%d  %H\:%M\:%S')),
            lasttimetabs = '\t' * 14,
            destdir      = '',
            comtabs      = '\t' * 3,
        )
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)

    def_list = ["DEF:%s=%s:%s:AVERAGE" % (dsname, params.get('rrdfile'), dsname) for dsname in ds]
    defs = ' \\\n\t'.join(def_list)
    params.setdefault('defs',defs)

    png_file = op.basename(params.get('rrdfile')).rsplit('.')[0] + '.png'
    params['filepath'] = op.join(params.get('destdir'), png_file)
    vdef = ["VDEF:{0}avg={0},AVERAGE",
            "VDEF:{0}max={0},MAXIMUM",
            "VDEF:{0}min={0},MINIMUM",
            "VDEF:{0}last={0},LAST"]

    graph_string = "AREA:{0}#{1}:\"{2} {0}\""
    gprint_choice1 = [ 
                "GPRINT:{0}last:\"%6.2lf %Sbps\"",
                "GPRINT:{0}max:\"%6.2lf %Sbps\"",
                "GPRINT:{0}min:\"%6.2lf %Sbps\"",
                "GPRINT:{0}avg:\"%6.2lf %Sbps\l\""]

    gprint_choice2 = [ 
                "GPRINT:{0}last:\"%8.2lf\"",
                "GPRINT:{0}max:\"%8.2lf\"",
                "GPRINT:{0}min:\"%8.2lf\"",
                "GPRINT:{0}avg:\"%8.2lf\l\""]
    X = params.get('X')
    gprint = gprint_choice2 if X == 0 else gprint_choice1
    vdef_list = []
    gprint_list = []
    for dsname in ds:
        for vdef_string in vdef:
            vdef_string = vdef_string.format(dsname)
            vdef_list.append(vdef_string)
        graph_string_temp = graph_string.format(dsname, colors(), params.get('legendprefix', 'legend'))
        gprint_list.append(graph_string_temp)
        for gprint_string in gprint:
            gprint_string = gprint_string.format(dsname)
            gprint_list.append(gprint_string)

    vdefs = ' \\\n\t'.join(vdef_list)
    gprints = ' \\\n\t'.join(gprint_list)
    params.setdefault('vdefs', vdefs)
    params.setdefault('gprints', gprints)
    cmd2 =  cmd.format(**params)
    os.system(cmd2)






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
                print file_path
#                graph(file_path, 'usage', 'free', title='memory usage', legendprefix='memory', destdir=destdir,)
                graph(file_path, 'free', 'usage', title='memory usage', legendprefix='memory', destdir=destdir,)
            elif re.search('load', filename):
                graph(file_path, 'load01', 'load05', 'load15', title='Load Average', legendprefix='CPU', destdir=destdir, X=0, comtabs='\t\t')
#            elif re.search('wlan0', filename):
#                graph(file_path, 'out', 'in', title="traffic wlan0", legendprefix='wlan0', destdir=destdir, X=9)
            elif fnmatch.fnmatch(filename, 'traffic_*.rrd'):
                legendprefix = filename[:-4].split('_')[1]
                title = 'traffic  %s' % legendprefix
                graph(file_path, 'out', 'in', title=title, legendprefix=legendprefix, destdir=destdir, X=6,)





if __name__ == '__main__':
#    graph('Memory.rrd', 'Memory_Free', 'Memory_Usage',)
    walk_graph('/data/django_serverauto/ServerAutoSys/rra/127.0.0.1', '/tmp')
