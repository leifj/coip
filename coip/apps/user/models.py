'''
Created on Jul 5, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name, lookup
from coip.apps.membership.models import add_member
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

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

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    home = models.ForeignKey(Name,blank=True,null=True,editable=False)
    identifier = models.ForeignKey(Identifier,editable=False,blank=True,null=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.user.__unicode__())

@receiver(post_save,sender=User)
def _create_profile(sender,**kwargs):
    user = kwargs['instance']
    created = kwargs['created']
    if created:
        profile,profile_created = UserProfile.objects.get_or_create(user=user)
        urn = lookup("urn",True)
        anyuser = lookup("system:anyuser",True)
        urn.setacl(anyuser,'rl')
        profile.home = lookup('user:'+user.username,autocreate=True)
        add_member(profile.home,user,hidden=True)
        profile.home.setpacl(profile.home, "rwlida")
        profile.home.setacl(profile.home,"rwla") #don't allow users to delete or reset acls on their home, nor invite members - that would be confusing as hell
        profile.home.short = user.get_full_name()
        profile.home.save()
        profile.save()
        
      
