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
    user = models.ForeignKey(User,unique=True,blank=True,related_name='user')
    inviter = models.ForeignKey(User,unique=True,blank=True,related_name='inviter')
    name = models.ForeignKey(Name,related_name='memberships')
    email = models.EmailField(blank=True,null=True)
    nonce = models.CharField(max_length=255,blank=True,null=True)
    enabled = models.BooleanField()
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True)
    
    def __unicode__(self):
        return "%s in %s" % (self.user,self.name)
    
    def valid(self):
        return self.enabled and datetime.date.today() > self.expires
    
    def status(self):
        if self.valid():
            return "active"
        else:
            return "inactive";
        
    def send_email(self):
        pprint("sent email to "+self.to)
        return
        
