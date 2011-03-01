'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
from pprint import pformat
import logging
from coip.apps.service.models import Service

class Membership(models.Model):
    '''
    Membership in a namespace/group
    '''
    user = models.ForeignKey(User,blank=True,null=True,related_name='user')
    service = models.ForeignKey(Service,blank=True,null=True,related_name='service')
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
        
    def is_user(self):
        return self.user != None
    
    def is_service(self):
        return self.service != None
    
def add_member(name,userorservice,hidden=False):
    if isinstance(userorservice,User):
        (m,created)  = Membership.objects.get_or_create(user=userorservice,name=name)
    else:
        (m,created)  = Membership.objects.get_or_create(service=userorservice,name=name)
        
    if created or not m.enabled or m.hidden != hidden:
        m.enabled = True
        m.hidden = hidden
        m.save()
        
def disable_member(name,userorservice):
    if isinstance(userorservice,User):
        m = Membership.objects.get(name=name,user=userorservice)
    else:
        m = Membership.objects.get(name=name,service=userorservice)
    if m:
        m.enabled = False
        m.save()
        
def remove_member(name,userorservice):
    if isinstance(userorservice,User):
        m = Membership.objects.get(name=name,user=userorservice)
    else:
        m = Membership.objects.get(name=name,service=userorservice)
    if m:
        m.delete()
        
def has_member(name,userorservice):
    if isinstance(userorservice,User):
        return Membership.objects.filter(name=name,user=userorservice)
    else:
        return Membership.objects.filter(name=name,service=userorservice)