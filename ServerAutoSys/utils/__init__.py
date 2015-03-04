#-*- coding: utf-8 -*-
import pexpect
from ansible.runner import Runner
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *
from modules.sshauth import add_keys
#from modules.graph import walk_graph
from modules.graph_shell import walk_graph
from modules.create_shell import walk_create

def AddKeyAuthenticate(username,passwd,host,port,
        public_key_file = SSH_PUBLIC_KEY_FILE,
        logfile = ADD_KEY_AUTH_LOG,):
    pattern = [
        '(?i)Connection refused',
        '(?i)Permission denied',
        '(?i)No route to host',
        '(?i)try logging into the machine',
        pexpect.EOF,
        pexpect.TIMEOUT,
        '(?i)Are you sure you want to continue connecting',
        '(?i)password:',
    ]

    message = [
        'Connection refused! Please check ssh Port',
        'Permission denied! Please check ssh password',
        'No route to host! Please check network',
        'Add key authentication success',
        'Not match! please check again',
        'TIMEOUT',
    ]        
    info = {'res': False, 'msg': ''}
    fout = file(logfile,'a+')
    child = pexpect.spawn('/usr/bin/ssh-copy-id -i %s "-p %s %s@%s"' % (public_key_file,port,username,host))
    child.logfile = fout
    index = ''
    while True:
        index = child.expect(pattern)
        if index == 3:
            info['res'] =True
            break
        elif index == 6:
            child.sendline('yes')
        elif index == 7:
            child.sendline(passwd)
        else:
            break
    info['msg'] = message[index]
    return info
        
#print AddKeyAuthenticate('root','123456','AddKeyAuthenticate.log',SSH_PUBLIC_KEY_FILE,'192.168.56.9',5000)

def ansible_transform(resultDic,hosts):
    resultList = {'success': [], 'failed': [], 'warning': []}
    for hostname, result in resultDic['contacted'].items():
        failed = result.get('failed', '')
        rc = result.get('rc', '')
        changed = result.get('changed', '')
        module_name = result.get('invocation', '').get('module_name', '')
        if hostname in hosts:
            hosts.remove(hostname)
        if rc == 0 and changed == True:
            stdout =  result.get('stdout', '') if result.get('stdout', '') else 'execute success'
            resultList['success'].append({hostname: stdout})
        elif failed == True:
            msg = result.get('msg', '')
            resultList['failed'].append({hostname: msg})
        elif changed == True and module_name in ['copy', 'fetch']:
            resultList['success'].append({hostname: 'success'})
        else:
            results = result.get('results', '')
            msg = result.get('msg', '')
            stderr = result.get('stderr', '')
            if results:
                res_stdout = results
            elif msg:
                res_stdout = msg
            elif stderr:
                res_stdout = stderr
            else:
                res_stdout = 'execute failed'
            resultList['failed'].append({hostname: res_stdout})

    for hostname, result in resultDic['dark'].items():
        if hostname in hosts:
            hosts.remove(hostname)
        if 'failed' in result:
            resultList['failed'].append({hostname: result['msg']})

    if hosts:
        for hostname in hosts:
            resultList['warning'].append(hostname)
    return resultList


def RunShellCmd(
        commands,
        pattern,
        module_name,
        host_list = ANSIBLE_HOST_FILE,
        private_key_file = SSH_PRIVATE_KEY_FILE,
        timeout = DEFAULT_TIMEOUT,
        forks = MAX_FORKS,
        ):
    host_num = len(host_list.split(';'))
    forks = host_num if host_num < forks else forks
    runResult = Runner(
        host_list = host_list,
        module_name = module_name,
        module_args = commands,
        forks = forks,
        timeout = timeout,
        pattern = pattern,
        private_key_file = private_key_file,
    ).run()
    print  runResult
    return runResult
#print ansible_transform(RunShellCmd('df -h','zabb','shell'))
