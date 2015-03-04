from django.db import models

# Create your models here.

class ServerGroup(models.Model):
#    id = models.IntegerField(primary_key=True)
    server_groupname = models.CharField(max_length = 50,unique = True)
    class Meta:
        db_table = u'server_group'

    def __unicode__(self):
        return self.server_groupname



class ServerList(models.Model):
#    id = models.BigIntegerField(primary_key=True)
    server_ip = models.CharField(max_length = 20,unique = True,verbose_name = 'remote IP')
    server_name = models.CharField(max_length = 50,verbose_name = 'remote hostname',unique = True)
    server_port = models.IntegerField(default = 22,verbose_name = 'ssh port')
    server_user = models.CharField(max_length = 20,default = 'root',verbose_name = 'ssh login user')
    server_pass = models.CharField(max_length = 50,verbose_name = 'ssh login password')
    is_choice = ((0,'N'),(1,'Y'))
    server_is_login = models.IntegerField(default = 0,choices = is_choice,verbose_name = 'is login(Y/N)?')
    server_snmp_on = models.IntegerField(default=0, choices=is_choice, verbose_name='snmp on(Y/N)?')
    server_groupname = models.ForeignKey('ServerGroup',db_column = 'server_group_id', verbose_name = 'group name')

    class Meta:
        db_table = u'server_list'

    def __unicode__(self):
        return self.server_ip


#class ServerRemoteuser(models.Model):
#    username = models.CharField(max_length = 20)
#    passwd = models.CharField(max_length = 50)
#    server_ip = models.ForeignKey('ServerList',db_column = 'server_list_id')
#
#    class Meta:
#        db_table = u'server_remoteuser'
#
#    def __unicode__(self):
#        return self.server_ip
#
