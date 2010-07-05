'''
Created on Jun 23, 2010

@author: leifj
'''

from django.db import models
from django.contrib.auth.models import User
from coip.apps.membership.models import Membership
from pprint import pprint
from uuid import uuid4
import datetime

class Invitation(models.Model):
    '''
    Represents an invitation to an application
    '''
    sender = models.ForeignKey(User, unique=True)
    membership = models.ForeignKey(Membership, unique=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField()
    token = models.TextField(unique=True)
    
    
    def __init__(self):
        self.token = uuid4()
        
    def valid(self):
        return datetime.date.today() > self.expires
    
    def send_email(self):
        pprint("sent email to "+self.to)
        return