'''
Created on Jun 23, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
from coip.apps.name.models import Name
import datetime
from pprint import pprint
from django.core.mail import send_mail
from coip.apps.userprofile.models import last_used_profile

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
        pinviter = last_used_profile(self.inviter)
        send_mail('[coip] Invitation to join \'%s\'' % (self.name.short), 
                  '''
                  
                  %s (%s) has invited you to join \'%s\':
                  
                  %s
                  
                  If you want to accept the invitation open this link in your browser:
                  
                  http://localhost/invitation/%s/accept
                  
                  To view information about \'%s\' open this link in your browser:
                  
                  http://localhost/name/%s
                  
                  ''' % (pinviter.display_name,pinviter.identifier,self.name.short,self.message,self.nonce,self.name.id),
                  'noreply@coip.example.com',[self.email], fail_silently=False)

        pprint("sent email to %s" % (self.email))
        return
        
