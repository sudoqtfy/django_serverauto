from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template.loader import get_template
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.views import login, logout
import json
import re
import os
import logging
from utils import AddKeyAuthenticate, ansible_transform, RunShellCmd, walk_graph
from app.models import ServerGroup,  ServerList
from utils.MachineStatus import *
from app.tasks import add_keys_task

#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)
logger = logging.getLogger(__name__)


@login_required
def index(request):
    logger.info('index')
#    if not request.user.is_authenticated():
#        login(request)
#    return HttpResponse(request.user.is_authenticated())
    return render_to_response('index.html')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index')
    return render_to_response('login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def executeCommand(request):
    if request.is_ajax():
        ip = request.POST.get('ip', '')
        hosts = request.POST.get('hosts', '')
        commands = request.POST.get('commands', '')
        module = request.POST.get('module', '')
        if ip and hosts and commands and module:
            lhosts = re.split(r'\s*;\s*', hosts)
            response = ansible_transform(RunShellCmd(commands, hosts, module), lhosts)
            print response
            return HttpResponse(json.dumps(response))
        else:
            logger.warning('Post data is empty!!!')
            return HttpResponse('')
    return render(request, 'exec_command.html')


@login_required
def getAllServerGroup(request):
    l = []
    for obj in ServerGroup.objects.all():
        d = {'name': obj.server_groupname, 'children': []}
        ServerListobj = ServerList.objects.filter(server_groupname=obj.id)
        l1 = []
        for obj1 in ServerListobj:
            print obj1
            d1 = {
                'ip': obj1.server_ip,
                'name': obj1.server_name,
                'port': obj1.server_port,
                'user': obj1.server_user,
                }
            l1.append(d1)
        d['children'] = l1
        l.append(d)
    print l
    return HttpResponse(json.dumps(l))


def doKeyAuth(request):
    id = request.GET.get('id', '')
    if id:
        ServerListobj = ServerList.objects.get(id=id)
    if ServerListobj:
        user = ServerListobj.server_user
        passwd = ServerListobj.server_pass
        ip = ServerListobj.server_ip
        port = ServerListobj.server_port
        info = AddKeyAuthenticate(user, passwd, ip, port)
        print info
        if info['res']:
            obj = ServerList.objects.get(id=id)
            obj.server_is_login = 1
            obj.save()
        return HttpResponse(json.dumps(info))
    else:
        return HttpResponse(json.dumps({'res': false, 'msg': 'server no found!'}))


@login_required
def batchAddKeyAuth(request):
    if request.method == 'POST':
        info = {'success': [], 'failed': []}
        serverStr = request.POST.get('serverStr', '')
        if  not serverStr:
            info['failed'].append({'no hostname found': 'empty'})
            return HttpResponse(json.dumps(info))
        server_list = serverStr.splitlines()
        for server in server_list:
            if re.match('#', server):
                continue
            sd = re.split(r'\s*\|\s*', server)
            if len(sd) != 6:
                info['failed'].append({server: 'Incorrect format'})
                continue
            try:
                ServerGroupObj = ServerGroup.objects.get(server_groupname = sd[5])
            except Exception,e:
                info['failed'].append({server: 'Can not find the group[%s]' % str(e)})
                continue
            d = {'server_ip': sd[0], 'server_name': sd[1], 'server_user': sd[2], 'server_pass': sd[3], 'server_port': sd[4], 'server_groupname': ServerGroupObj, 'server_is_login': 0}
            ServerListobj = ServerList(**d)
            try:
                ServerListobj.save()
                info['success'].append(sd[1])
                add_keys_task.delay(sd[0], sd[2], sd[3], sd[4], [settings.SSH_PUBLIC_KEY_FILE])
            except Exception,e:
                info['failed'].append({server: 'save error[%s]' % str(e)})
                continue
        print info
        return HttpResponse(json.dumps(info))
    return render(request, 'add_server_list.html')


@login_required
def getServerList(request):
    server_list = ServerList.objects.all()
    p = Paginator(server_list, settings.PAGE_SIZE)
    page = request.GET.get('page', 1)
    print server_list
    try:
        server_list = p.page(page)
    except (EmptyPage, InvalidPage):
        server_list = p.page(p.num_pages)
    d = {'server_list': server_list}
    return render(request, 'server_list.html', d)


def graph(request):

    return  render(request, 'graph.html')


def graph_list(request):
    ip = request.GET.get('ip', '')
    if ip:
        htmls = ''
        html = '''
                     <div  class="center" >
                         <img src="/static/rra/{0}" />
                     </div>
                     <hr>
               '''
        print ip
        rrd_dir = '/data/django_serverauto/ServerAutoSys/rra/' + ip
        png_dir = '/data/django_serverauto/ServerAutoSys/static/rra/' + ip
        try:
            walk_graph(rrd_dir, png_dir)
        except Exception as e:
            logger.exception('walk_graph error', e)
        if os.path.isdir(png_dir):
            img_list = os.listdir(png_dir)
        else:
            img_list = []
#        img_list = ['Flow.png'] * 5
        if len(img_list) == 0:
            return HttpResponse('')
        for img in img_list:
            htmls += html.format(ip+'/'+img)
        return HttpResponse(htmls)

    slist = []
    for group in ServerGroup.objects.all():
        group_dict = {'n': group.server_groupname, 'c': []}
        list_objs = ServerList.objects.filter(server_groupname=group, server_snmp_on=1)
        if len(list_objs) == 0: continue
        for list_obj in list_objs:
            group_dict['c'].append('{0}_{1}'.format(list_obj.server_ip,list_obj.server_name))
        slist.append(group_dict)
    return HttpResponse(json.dumps(slist))


def getPercentInfo(request):
    d = get_percent_info()
    print d
    return HttpResponse(json.dumps(d))


def getMemInfo(request):
    d = get_mem_info()
    print d
    return HttpResponse(json.dumps(d))


def getLoadAvg(request):
    d = get_load_avg()
    print d
    d = ','.join(['"%s":%s' % (k,  v) for k,  v in d.items()])
    return HttpResponse('{%s}' % d)


def getCpuInfo(request):
    d = get_cpu_info()
    print d
    d = ','.join(['"%s":%s' % (k,  v) for k,  v in d.items()])
    return HttpResponse('{%s}' % d)


def getDiskInfo(request):
    d = get_disk_info()
    print d
    d = ','.join(['"%s":%s' % (k,  v) for k,  v in d.items()])
    return HttpResponse('{%s}' % d)


def getNetInfo(request):
    d = get_network_info()
    print d
    d = ','.join(['"%s":%s' % (k,  v) for k,  v in d.items()])
    return HttpResponse('{%s}' % d)
