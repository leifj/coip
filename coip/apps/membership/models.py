'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
from pprint import pprint

class Membership(models.Model):
    '''
    Membership in a namespace/group
    '''
    user = models.ForeignKey(User,blank=True,null=True,related_name='user')
    name = models.ForeignKey(Name,related_name='memberships')
    enabled = models.BooleanField()
    hidden = models.BooleanField()
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True,null=True)
    
    def __unicode__(self):
        return "%s in %s" % (self.user,self.name)
    
    def valid(self):
        return self.enabled and datetime.date.today() > self.expires
    
    def status(self):
        if self.valid():
            return "active"
        else:
            return "inactive";
    
def add_member(name,user):
    (m,created)  = Membership.objects.get_or_create(user=user,name=name)
    if created or not m.enabled:
        m.enabled = True
        m.save()
        
def disable_member(name,user):
    m = Membership.objects.get(name=name,user=user)
    if m:
        m.enabled = False
        m.save()
        
def remove_member(name,user):
    m = Membership.objects.get(name=name,user=user)
    if m:
        m.delete()
        
