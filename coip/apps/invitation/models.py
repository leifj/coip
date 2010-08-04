'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
from pprint import pprint

class Invitation(models.Model):
    '''
    Invitation to a namespace/group
    '''
    inviter = models.ForeignKey(User,related_name='inviter')
    name = models.ForeignKey(Name,related_name='invitations')
    email = models.EmailField()
    message = models.TextField()
    nonce = models.CharField(unique=True,max_length=255)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField()
    
    def __unicode__(self):
        return "%s invited to %s by %s" % (self.email,self.name,self.inviter)
        
    def send_email(self):
        pprint("sent email to %s" % (self.email))
        return
        
