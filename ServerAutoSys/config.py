# config file
import os
import logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'utils')
LOG_DIR = os.path.join(BASE_DIR, 'log')
# Database
DB_NAME = 'ServerAutoSys'
DB_USER = 'root'
DB_PASS = 'root'
DB_PORT = '3306'
DB_HOST = '127.0.0.1'
# FORKS
MAX_FORKS = 10
# TIMEOUT
DEFAULT_TIMEOUT = 20
# ssh public key path
SSH_PUBLIC_KEY_FILE = os.path.expanduser('~/.ssh/id_rsa.pub')
SSH_PRIVATE_KEY_FILE = os.path.expanduser('~/.ssh/id_rsa')
# ansible
ANSIBLE_HOST_FILE = os.path.join(PUBLIC_DIR, 'hosts')
# log file
ADD_KEY_AUTH_LOG = os.path.join(LOG_DIR, 'AddKeyAuthenticate.log')
LOG_FILE = os.path.join(LOG_DIR, 'ServerAutoSys.log')
# page
PAGE_SIZE = 5
'''
logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s [%(levelname)s] %(message)s',
                    filename = os.path.join(LOG_DIR, 'ServerAutoSys.log'),
                    filemode = 'a')
'''
