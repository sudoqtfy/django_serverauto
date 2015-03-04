#!/usr/bin/env python
import inspect
import os, time, socket

class Mon:
    def __init__(self):
        self.data = {}


    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            return "%s %s %s" % (a[0],a[1],a[2])
#            return   float(a[0])
    

    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a / 1024
    

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (T-F-B-C) * 1024
        else:
            with open('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a * 1024
    

    def getMemFree(self, noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F+B+C) * 1024
        else:
            with open('/proc/meminfo') as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1])
                return a * 1024
    

    def getHost(self):
        return socket.gethostname()


    def getTime(self):
        return int(time.time())


    def getTraffic(self):
        traffic_dict = {}
        with open('/proc/net/dev') as f:
            ifstat = f.readlines()
            ifstat.pop(0)
            ifstat.pop(0)
        for interface in ifstat:
            ifc_name = interface.split(':')[0].strip()
            if ifc_name.strip() == 'lo': continue
            ifc_out = interface.split(':')[1].split()[8].strip()
            ifc_in = interface.split(':')[1].split()[0].strip()
            traffic_dict[ifc_name] = "%s:%s" % (ifc_out, ifc_in)
        return traffic_dict
        


    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data

if __name__ == "__main__":
    print Mon().runAllGet()
