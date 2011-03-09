'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
import logging
from coip.apps.entity.models import Entity
import tagging
from django.core.mail import send_mail
from coip.settings import NOREPLY

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
    
    def send_notification(self,what):
        if not self.user or not self.user.email:
            return
                
        send_mail('You have been %s \'%s\'' % (what,self.name.short),
                  '''
You have been %s \'%s\'.

To view information about \'%s\' open this link in your browser:
%s

''' % (what,self.name.shortname(),self.name.shortname(),self.name.url()),
                  NOREPLY,
                  [self.user.email], 
                  fail_silently=False)
        return
    
def add_member(name,member_name,hidden=False):
    if isinstance(member_name,User):
        (m,created)  = Membership.objects.get_or_create(user=member_name,name=name)
    else:
        (m,created)  = Membership.objects.get_or_create(entity=member_name,name=name)
        
    if created or not m.enabled or m.hidden != hidden:
        m.enabled = True
        m.hidden = hidden
        m.save()
    
    return m.send_notification("added to")
        
def disable_member(name,member_name):
    if isinstance(member_name,User):
        m = Membership.objects.get(name=name,user=member_name)
    else:
        m = Membership.objects.get(name=name,entity=member_name)
    if m:
        m.enabled = False
        m.save()
        m.send_notification("temporarily removed from")
        
def remove_member(name,member_name):
    if isinstance(member_name,User):
        m = Membership.objects.get(name=name,user=member_name)
    else:
        m = Membership.objects.get(name=name,entity=member_name)
    if m:
        m.send_notification("removed from")
        m.delete()
        
def has_member(name,member_name):
    if isinstance(member_name,User):
        return Membership.objects.filter(name=name,user=member_name)
    else:
        return Membership.objects.filter(name=name,entity=member_name)

tagging.register(Membership)