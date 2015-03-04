from celery import task
from utils import add_keys, walk_create
from app.models import ServerList
#python manage.py celery worker --loglevel=info
#python manage.py celery flower --address=192.168.56.155



@task
def add_keys_task(host, user, password, port=22, key_files = []):
    if add_keys(host, user, password, key_files, port):
        server_list = ServerList.objects.get(server_ip=host)
        print server_list
        if server_list:
            server_list.server_is_login = 1
            server_list.save()
            
@task
def walk_create_task(filepath):
    walk_create(filepath)
