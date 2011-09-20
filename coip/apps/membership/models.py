'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
import tagging
from django.core.mail import send_mail
from coip.settings import NOREPLY
from coip.extensions.templatetags.userdisplay import userdisplay
from coip.apps.userprofile.models import UserProfile

STATUS = {UserProfile.INTERNAL:'internal',
          UserProfile.ENTITY:'entity',
          UserProfile.SSHKEY:'sshkey',
          UserProfile.X509:'certificate',
          UserProfile.FEDID:'fedid'}

class Membership(models.Model):
    '''
    Membership in a namespace/group
    '''
    user = models.ForeignKey(User,related_name='memberships')
    name = models.ForeignKey(Name,related_name='memberships')
    enabled = models.BooleanField()
    hidden = models.BooleanField()
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True,null=True)
    
    def __unicode__(self):
        who = self.user    
        status = ""
        if not self.enabled:
            status = " (disabled)"
        hidden = ""
        if self.hidden:
            hidden = " (hidden)"
        return "%s in %s%s%s" % (who,self.name,status,hidden)
    
    def valid(self):
        return self.enabled and datetime.date.today() > self.expires
    
    def status(self):
        if self.valid():
            return "active"
        else:
            return "inactive";
    
    def type(self):
        return STATUS[self.user.get_profile().type]
    
    def send_notification(self,what):
        if not self.user or not self.user.email:
            return
        
        send_mail('%s have been %s \'%s\'' % (userdisplay(self.user),what,self.name.short),
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
    (m,created)  = Membership.objects.get_or_create(user=member_name,name=name)
    if created or not m.enabled or m.hidden != hidden:
        m.enabled = True
        m.hidden = hidden
        m.save()
        
    if name.nmembers != -1:
        name.nmembers = -1
        name.save()
    
    return m.send_notification("added to")
        
def disable_member(name,member_name):
    m = Membership.objects.get(name=name,user=member_name)
    if m:
        m.enabled = False
        m.save()
        m.send_notification("temporarily removed from")
        
    if name.nmembers != -1:
        name.nmembers = -1
        name.save()
        
def remove_member(name,member_name):
    m = Membership.objects.get(name=name,user=member_name)
    if m:
        m.send_notification("removed from")
        m.delete()
    
    if name.nmembers != -1:
        name.nmembers = -1
        name.save()
        
def has_member(name,member_name):
    return Membership.objects.filter(name=name,user=member_name)

tagging.register(Membership)