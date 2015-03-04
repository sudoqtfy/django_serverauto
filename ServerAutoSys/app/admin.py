from django.contrib import admin
from app.models import ServerGroup, ServerList
# Register your models here.


class ServerGroupAdmin(admin.ModelAdmin):
    list_display = ('id',  'server_groupname')


class ServerListAdmin(admin.ModelAdmin):
    list_display = ('id', 'server_ip', 'server_name', 'server_port', 'server_user', 'server_pass', 'server_is_login', 'server_snmp_on', 'server_groupname')

#class ServerRemoteuserAdmin(admin.ModelAdmin):
#    list_display = ('username', 'passwd', 'server_ip')

admin.site.register(ServerGroup, ServerGroupAdmin)
admin.site.register(ServerList, ServerListAdmin)
#admin.site.register(ServerRemoteuser, ServerRemoteuserAdmin)
