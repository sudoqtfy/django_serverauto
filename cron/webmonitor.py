#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
activate_this = '/data/django_serverauto/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
#from django.db import connection, transaction
import sys
import time
import logging
from decimal import Decimal
sys.path.append(os.path.dirname(CUR_PATH))
from config import LOG_DIR
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from web.models import *
import pycurl
logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s [%(levelname)s] %(message)s',
                    filename = 'webmonitor.log',
                    filemode = 'a')

CONNECTTIMEOUT = 5
TIMEOUT = 5


class CurlObj():

    def __init__(self):
        self.Curlobj = pycurl.Curl()

    def _setOpt(self, url):
        self.Curlobj.setopt(self.Curlobj.URL, url)
        self.Curlobj.setopt(self.Curlobj.CONNECTTIMEOUT, CONNECTTIMEOUT)
        self.Curlobj.setopt(self.Curlobj.TIMEOUT, TIMEOUT)
        self.Curlobj.setopt(self.Curlobj.NOPROGRESS, 0)
        self.Curlobj.setopt(self.Curlobj.FOLLOWLOCATION, 1)
        self.Curlobj.setopt(self.Curlobj.MAXREDIRS, 5)
        self.Curlobj.setopt(self.Curlobj.OPT_FILETIME, 1)
        self.Curlobj.setopt(self.Curlobj.NOPROGRESS, 1)
        bodyfile = open(os.path.join(LOG_DIR, 'body_html.log'), "wb")
        self.Curlobj.setopt(self.Curlobj.WRITEDATA, bodyfile)
        self.Curlobj.perform()
        bodyfile.close() 
        

    def _getInfo(self, url, CONNECTTIMEOUT = 20, TIMEOUT = 20):
        self._setOpt(url)
        d = {}
        d['NAMELOOKUP_TIME'] = Decimal(str(round(self.Curlobj.getinfo(self.Curlobj.NAMELOOKUP_TIME), 2)))
        d['CONNECT_TIME']    = Decimal(str(round(self.Curlobj.getinfo(self.Curlobj.CONNECT_TIME),2)))
        d['TOTAL_TIME']      = Decimal(str(round(self.Curlobj.getinfo(self.Curlobj.TOTAL_TIME),2)))
        d['HTTP_CODE']       = self.Curlobj.getinfo(self.Curlobj.HTTP_CODE)
        d['SPEED_DOWNLOAD']  = self.Curlobj.getinfo(self.Curlobj.SPEED_DOWNLOAD)
        return d


    def _getHost(self):
        webinfoobj = WebInfo.objects.all()
        if webinfoobj is not None:
            return webinfoobj
        return false


    def runPyCurl(self):
        hosts =  self._getHost()
        if not hosts: 
            logging.warning('no data found!')
        for host in hosts:
            try:
                d = self._getInfo(host.URL)
            except Exception,e:
                logging.error("couldn't connect to host")
                continue
            d['DATETIME'] = time.strftime('%s')
            d['webinfo_id'] = host
            print d
            webinfo = WebData(**d)
            webinfo.save()



if __name__ == '__main__':
    c = CurlObj()
    c.runPyCurl()
