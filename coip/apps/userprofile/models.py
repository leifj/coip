'''
Created on Jul 5, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name, lookup
from coip.apps.membership.models import add_member

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    home = models.ForeignKey(Name,blank=True,null=True,editable=False)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.user.__unicode__())
    

def user_profile(user):
    profile,created = UserProfile.objects.get_or_create(user=user)
    if created:
        urn = lookup("urn",True)
        anyuser = lookup("system:anyuser",True)
        urn.setacl(anyuser,'rl')
        home = lookup('user:'+user.username,autocreate=True)
        home.short = user.get_full_name()
        profile.home = home
        profile.save()
        home.save()
        add_member(home,profile.user,hidden=True)
        home.setpacl(home, "rwlida")
        home.setacl(home,"rwla") #don't allow users to delete or reset acls on their home, nor invite members - that would be confusing as hell
    
    return profile

class Identifier(models.Model):
    
    FEDERATION=0
    EMAIL=1
    SSHKEY=2
    GRIDCERT=3
    INTERNAL=4
    
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(User,related_name='identifiers')
    display_name = models.CharField(max_length=255,blank=True,null=True)
    type = models.SmallIntegerField(default=0,choices=((0,'Federation Identifier'),(1,'Email Address'),(2,'SSH Key'),(3,'eScience Certificate'),(4,'Internal User')))
    idp = models.CharField(max_length=255,blank=True,null=True)
    verified = models.BooleanField()
    value = models.CharField(max_length=1023)
    verification_code = models.CharField(max_length=1023,blank=True,null=True)
    
    #class Meta:
    #    unique_together = ('value','idp')
        
    def __unicode__(self):
        return "%s [%s]" % (self.value,self.display_name)
