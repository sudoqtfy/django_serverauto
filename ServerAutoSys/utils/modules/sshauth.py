#!/usr/bin/env python

from sh import scp, ssh, ErrorReturnCode_1, ErrorReturnCode_255
import os
import sys
import os.path as op
import logging
from getpass import getpass
from tempfile import NamedTemporaryFile
#logging.basicConfig(format='%(message)s', level=logging.INFO)


class NoSuchFileError(Exception):
    pass




def load_local_keys(key_files=['~/.ssh/id_rsa.pub']):
    '''read local public key'''
    if len(key_files) == 0:
        key_files.append('~/.ssh/id_rsa.pub')

    key_dict = {}
    for key_file in key_files:
        with open(op.expanduser(key_file)) as f:
            key_con = f.read().strip()
            key_dict.setdefault(key_file,key_con)

    return key_dict


class SHController(object):
    
    user = None
    host = None
    port = 22
    
    def __init__(self, host, user, port=22):
        self.out = b''
        self.host = host
        self.user = user
        self.port = port if port else 22
        self._password = None
    

    def __call__(self, *args, **kwargs):
        logging.info('run command: "{0}"'.format(self.process.ran))
        self.process.wait()


    def ssh_iteract(self, char, stdin, process):
#        print char
        if isinstance(char, str):
            self.out += char.encode('utf8')
        else:
            self.out += char
        out = self.out.decode('utf-8')
        if out.endswith('password:'):
            self.out = b''
            stdin.put(self.password+'\n')



    @property
    def password(self):
        logging.info('require password')
        return self._password
        
    
    @password.setter
    def password(self, value):
        self._password = value
    


class SSHController(SHController):
    no_such_file_error = False

    def __call__(self, *args, **kwargs):
        self.process = ssh(
                            '-o UserKnownHostsFile=/dev/null',
                            '-o StrictHostKeyChecking=no',
                            '-o LogLevel=quiet',
                            '{0}@{1}'.format(self.user, self.host),
                            '-p', self.port,
                            'LANG=C', *args,
                            _out=self.ssh_iteract, _out_bufsize=0, _tty_in=True,
                            **kwargs)
        
        super(SSHController, self).__call__(*args, **kwargs)


    def ssh_iteract(self, char, stdin, process):
        super(SSHController, self).ssh_iteract(char, stdin, process)
        out = self.out.decode('utf8')
        if out.endswith('No such file or directory'):
            self.no_such_file_error = True
            process.kill()
            return True
        


class SCPController(SHController):

    def __call__(self, local_file, remote_file, **kwargs):
        self.process = scp(
                            '-o UserKnownHostsFile=/dev/null',
                            '-o StrictHostKeyChecking=no',
                            '-o LogLevel=quiet',
                            '-P', self.port,
                            local_file,
                            '{0}@{1}:{2}'.format(self.user, self.host, remote_file),
                            _out=self.ssh_iteract, _out_bufsize=0, _tty_in=True,
                            **kwargs)
        super(SCPController, self).__call__(local_file, remote_file, **kwargs)




def _get_authorized_keys(controller):
    logging.info('{c.user}@{c.host}:{c.port} -- get authorized_keys'.format(c=controller))
    
    try:
        controller('cat ~/.ssh/authorized_keys')
    except ErrorReturnCode_1:
        if controller.no_such_file_error:
            raise NoSuchFileError
        else:
            logging.critical(controller.out.decode('utf8'))
            raise
    except ErrorReturnCode_255:
        logging.critical(controller.out.decode('utf8'))
        raise
    
    out = controller.out.decode('utf8')

    return [line.strip() for line in out.strip().split(os.linesep) if line]

     

def _create_authorized_keys(controller):
    logging.info('{c.user}@{c.host}:{c.port} -- create .ssh file'.format(c=controller))

    try:
        controller('test -d ~/.ssh || mkdir ~/.ssh')
    except Exception:
        logging.critical(controller.out.decode('utf8'))
        raise


def _set_authorized_keys(controller, keys):
    logging.info('{c.user}@{c.host}:{c.port} -- set authorized_keys'.format(c=controller))

    if sys.version_info[0] >=3:
        buffering = 'buffering'
    else:
        buffering = 'bufsize'

    with NamedTemporaryFile('w+b', **{buffering: 0}) as temp:
        data = "\n".join(keys)
        temp.write(data.encode('utf8'))
        if data and data[-1] != '\n':
            temp.write('\n')

        try:
            controller(temp.name, '~/.ssh/authorized_keys')
        except Exception:
            logging.critical(controller.out.encode('utf8'))
            raise

def del_keys(host, user, password, port=22):
    pass
    


def add_keys(host, user, password, key_files=[], port=22):
    if len(key_files) == 0:
        local_keys = load_local_keys().values()
    else:
        local_keys = load_local_keys(key_files).values()

    ssh_controller = SSHController(host, user, port)
    ssh_controller.password = password
    try:
        remote_keys = _get_authorized_keys(ssh_controller)
        print len(remote_keys)
    except NoSuchFileError:
        _create_authorized_keys(ssh_controller)
        remote_keys = []
    except ErrorReturnCode_1:
        sys.exit(1)

    new_keys = list(set(local_keys+remote_keys))
    scp_controller = SCPController(host, user, port)
    scp_controller.password = password
    try:
        _set_authorized_keys(scp_controller, new_keys)
    except ErrorReturnCode_1:
        sys.exit(1)
    return True



def get_keys():
    pass

#add_keys('192.168.56.2', 'root', '123456', ['/home/django/.ssh/id_rsa.pub','~/.ssh/id_rsa.pub'])
#scp_controller = SCPController('192.168.56.130', 'root')
#scp_controller.password = '123456'
#_set_authorized_keys(scp_controller, load_local_keys().values())
#ssh_controller = SSHController("192.168.56.130", 'root')
#ssh_controller.password = '123456'
#print _get_authorized_keys(ssh_controller)
#_create_authorized_keys(ssh_controller)
#ssh_controller('test -d ~/.ssh || mkdir ~/.ssh')
#ssh_controller('cat  ~/.ssh/authorized_keys')
