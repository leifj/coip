'''
Created on Jul 5, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from coip.apps.name.models import Name

class UserProfile(models.Model):
    
    INTERNAL = 0
    ENTITY = 1
    SSHKEY = 2
    X509 = 3
    FEDID = 4
    
    #
    # User content
    # 0 (internal) - normal
    # 1 (entity)   - username=entity:sha1(entityID), profile.display_name = display or entityID, profile.identifier = ssh key
    # 2 (sshkey)   - username=sshkey:fingerprint, profile.display_name = key alias or "SSH Key with fingerprint ..."
    # 3 (gridcert) - username=x509:sha1-fingerprint, profile.display_name = dn, profile.identifier = PEM
    # 4 (fedid)    - username=eppn or equiv (REMOTE_USER),profile.display_name = display or eppn, profile.identifier = eppn, profile.idp = idp
    #
    
    user = models.OneToOneField(User,related_name='profile')
    home = models.ForeignKey(Name,blank=True,null=True)
    display_name = models.CharField(max_length=255,blank=True,null=True)
    type = models.SmallIntegerField(default=INTERNAL,
                                    choices=((ENTITY,"Service"),
                                             (INTERNAL,"System User"),
                                             (SSHKEY,"Personal SSH Key"),
                                             (X509,"Personal eScience Certificate"),
                                             (FEDID,"User Identity")))
    
    idp = models.CharField(max_length=255,blank=True,null=True)
    identifier = models.CharField(max_length=1023,blank=True,null=True)
    
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s [%s] - %s" % (self.identifier,self.user.username,self.display_name)

@receiver(post_save,sender=User)
def _create_profile(sender,**kwargs):
    user = kwargs['instance']
    UserProfile.objects.get_or_create(user=user)