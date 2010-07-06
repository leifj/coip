'''
Created on Jul 5, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,related_name='profiles')
    display_name = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    idp = models.CharField(max_length=255,blank=True,null=True)
    identifier = models.CharField(max_length=1023,unique=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s [%s] - %s" % (self.identifier,self.user.username,self.display_name)
    
class PKey(models.Model):
    user_profile = models.ForeignKey(UserProfile,related_name='keys')
    key = models.CharField(max_length=1023,unique=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "A merge-key for "+self.user_profile

    