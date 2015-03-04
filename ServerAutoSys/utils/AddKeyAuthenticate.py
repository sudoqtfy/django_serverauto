import pexpect
from multiprocessing import Process
import os
from celery import Celery
SSH_PUBLIC_KEY_FILE = '/root/.ssh/id_rsa.pub'

broker = 'redis://127.0.0.1/0'
backend = 'redis://127.0.0.1/1'

app = Celery('tasks', broker=broker, backend=backend)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
)

@app.task
def AddKeyAuthenticate(username,passwd,logfile,keyfile,host,port):
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
    info = {'res':False,'msg':''}
#    fout = file(logfile,'a+')
    child = pexpect.spawn('/usr/bin/ssh-copy-id -i %s "-p %s %s@%s"' % (keyfile,port,username,host))
#    child.logfile = fout
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
    print info
    return info
        
#print AddKeyAuthenticate('root','123456','AddKeyAuthenticate.log',SSH_PUBLIC_KEY_FILE,'192.168.56.130',22)



#def run_proc(name):
#    print 'Run child process %s (%s)...' % (name, os.getpid())
#
#if __name__=='__main__':
#    print 'Parent process %s.' % os.getpid()
#    p = Process(target=AddKeyAuthenticate, args=('root','123456','AddKeyAuthenticate.log',SSH_PUBLIC_KEY_FILE,'192.168.56.9',5000))
#    print 'Process will start.'
#    p.start()
#    p.join()
#    print 'Process end.'
