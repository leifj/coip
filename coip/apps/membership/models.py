'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime

class Membership(models.Model):
    '''
    Membership in a namespace/group
    '''
    user = models.ForeignKey(User,unique=True,blank=True)
    enabled = models.BooleanField()
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True)
    name = models.ForeignKey(Name,related_name='memberships')
    
    def __unicode__(self):
        return "%s in %s" % (self.user,self.name)
    
    def valid(self):
        return self.enabled and datetime.date.today() > self.expires
    
    def status(self):
        if self.valid():
            return "active"
        else:
            return "inactive";
