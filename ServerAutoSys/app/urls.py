from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.views',
    url(r'getMemInfo/$', 'getMemInfo'),
    url(r'getLoadAvg/$', 'getLoadAvg'),
    url(r'getCpuInfo/$', 'getCpuInfo'),
    url(r'getDiskInfo/$', 'getDiskInfo'),
    url(r'getNetInfo/$', 'getNetInfo'),
    url(r'getPercentInfo/$', 'getPercentInfo'),
    url(r'getServerList/$', 'getServerList'),
    url(r'doKeyAuth/$', 'doKeyAuth'),
    url(r'executeCommand/$', 'executeCommand'),
    url(r'getAllServerGroup/$', 'getAllServerGroup'),
    url(r'batchAddKeyAuth/$', 'batchAddKeyAuth'),
    url(r'graph/$', 'graph'),
    url(r'graph_list/$', 'graph_list'),
)
