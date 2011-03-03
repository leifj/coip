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
from coip.apps.entity.models import Entity

class Membership(models.Model):
    '''
    Membership in a namespace/group
    '''
    user = models.ForeignKey(User,blank=True,null=True,related_name='user')
    entity = models.ForeignKey(Entity,blank=True,null=True,related_name='entity')
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
    
    def is_entity(self):
        return self.entity != None
    
def add_member(name,member_name,hidden=False):
    if isinstance(member_name,User):
        (m,created)  = Membership.objects.get_or_create(user=member_name,name=name)
    else:
        (m,created)  = Membership.objects.get_or_create(entity=member_name,name=name)
        
    if created or not m.enabled or m.hidden != hidden:
        m.enabled = True
        m.hidden = hidden
        m.save()
        
def disable_member(name,member_name):
    if isinstance(member_name,User):
        m = Membership.objects.get(name=name,user=member_name)
    else:
        m = Membership.objects.get(name=name,entity=member_name)
    if m:
        m.enabled = False
        m.save()
        
def remove_member(name,member_name):
    if isinstance(member_name,User):
        m = Membership.objects.get(name=name,user=member_name)
    else:
        m = Membership.objects.get(name=name,entity=member_name)
    if m:
        m.delete()
        
def has_member(name,member_name):
    if isinstance(member_name,User):
        return Membership.objects.filter(name=name,user=member_name)
    else:
        return Membership.objects.filter(name=name,entity=member_name)