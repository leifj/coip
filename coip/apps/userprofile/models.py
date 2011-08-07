'''
Created on Jul 5, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name

class UserProfile(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,related_name='profiles')
    display_name = models.CharField(max_length=255,blank=True,null=True)
    primary = models.BooleanField()
    email = models.EmailField(blank=True,null=True)
    idp = models.CharField(max_length=255,blank=True,null=True)
    identifier = models.CharField(max_length=1023,unique=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    home = models.ForeignKey(Name,blank=True,null=True,editable=False)
    
    def __unicode__(self):
        return "%s [%s] - %s" % (self.identifier,self.user.username,self.display_name)

    def make_primary(self):
        for p in UserProfile.objects.filter(user=self.user).all:
            p.primary = False
        self.primary = True

def last_used_profile(user):
    return UserProfile.objects.filter(user=user).order_by('lastupdated')[0]

def primary_profile(user):
    return UserProfile.objects.filter(user=user,primary=True)[0]

    
class PKey(models.Model):
    user_profile = models.ForeignKey(UserProfile,related_name='keys')
    key = models.CharField(max_length=1023,unique=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "A merge-key for "+self.user_profile
