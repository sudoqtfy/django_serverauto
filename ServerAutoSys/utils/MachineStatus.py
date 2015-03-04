# -*- encoding: utf-8 -*-
 
import psutil
import socket
import uuid
import subprocess
 

#  获取mac
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    MAC = ":".join([mac[e : e+2] for e in range(0, 11, 2)])
    return {'MAC' : MAC}

#  获取ip
def get_ip_address():
    tempsutilock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tempsutilock.connect(('8.8.8.8', 80))
    addr = tempsutilock.getsockname()[0]
    tempsutilock.close()
    return {'IP' : addr}

#  获得cpu信息
def get_cpu_info():
    cpu = {'cores' : 0,            #  cpu逻辑核数
            'percent' : 0,          #  cpu使用率
            'system_time' : 0,      #  内核态系统时间
            'user_time' : 0,        #  用户态时间
            'idle_time' : 0,        #  空闲时间
            'nice_time' : 0,        #  nice时间 (花费在调整进程优先级上的时间)
            'softirq' : 0,          #  软件中断时间
            'irq' : 0,              #  中断时间
            'iowait' : 0}
    cpu['cores'] = psutil.cpu_count()
    cpu['percent'] = psutil.cpu_percent(interval=2)
    cpu_times = psutil.cpu_times()
    cpu['system_time'] = cpu_times.system
    cpu['user_time'] = cpu_times.user
    cpu['idle_time'] = cpu_times.idle
    cpu['nice_time'] = cpu_times.nice
    cpu['softirq'] = cpu_times.softirq
    cpu['irq'] = cpu_times.irq
    cpu['iowait'] = cpu_times.iowait
    return cpu

#  获得memory信息
def get_mem_info():
    mem = {'percent' : 0,
            'total' : 0,
            'vailable' : 0,
            'used' : 0,
            'free' : 0,
            'active' : 0}
    mem_info = psutil.virtual_memory()
    mem['percent'] = round(100 - mem_info.percent)
    mem['total'] = mem_info.total
    mem['vailable'] = mem_info.available
    mem['used'] = mem_info.used
    mem['free'] = mem_info.free
    mem['active'] = mem_info.active
    return mem

#  获取进程信息
def get_process_info():
    process = {'count' : 0,        #  进程数目
               'pids' : 0}         #  进程识别号
    pids = psutil.pids()
    process['pids'] = pids
    process['count'] = len(pids)
    return process

#  获取网络数据
def get_network_info():
    network = {'count' : 0,        #  连接总数
               'established' : 0}  #  established连接数
    conns = psutil.net_connections()
    network['count'] = len(conns)
    count = 0
    for conn in conns:
       if conn.status is 'ESTABLISHED':
           count = count + 1
    network['established'] = count
    return network

def get_load_avg():
    loadavg = subprocess.Popen('cat /proc/loadavg',shell=True,stdout=subprocess.PIPE).stdout.read().split()
    return {'m1':loadavg[0],'m5':loadavg[1],'m15':loadavg[2]}

def get_disk_info():
    disk_info = {'total':0,
                'used': 0,
                'percent': 0}
    disk_usage = psutil.disk_usage('/')
    disk_info['total'] = disk_usage.total
    disk_info['used'] = disk_usage.used
    disk_info['percent'] = round(disk_usage.percent,3)
    return disk_info

def get_percent_info():
    users = lambda: subprocess.Popen('cat /etc/passwd | wc -l', shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    groups = lambda: subprocess.Popen('cat /etc/group | wc -l', shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    ports = lambda(x): subprocess.Popen(r"netstat -tunlp | grep -c '%s'" % x, shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    web_port_status = '100' if ports('nginx|apache|httpd')!='0' else '0'
    redis_port_status = '100' if ports('redis-server')!='0' else '0'
    percent_info = {
            'disk_usage_per': get_disk_info().get('percent', ''),
            'memory_usage_per': get_mem_info().get('percent', ''),
            'count_users': users(),
            'count_groups': groups(),
            'web_port_status': web_port_status,
            'redis_port_status': redis_port_status,
            }
    return percent_info

if __name__ == '__main__':
    print get_cpu_info()
    print get_ip_address()
    print get_mac_address()
    print get_mem_info()
    print get_process_info()
    print get_network_info()
    print get_load_avg()
    print get_disk_info()
    print get_percent_info()
