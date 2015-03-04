from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ServerMonSys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.login'),
    url(r'^logout$', 'app.views.logout'),
    url(r'^index$', 'app.views.index'),
    url(r'^app/', include('app.urls')),
#    url(r'^accounts/login/', login, {'template_name': 'login.html'}),
)
