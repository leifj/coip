'''
Created on Feb 23, 2011

@author: leifj
'''

from django.db import models
import re
from pprint import pformat
import logging
from django.db.models.fields import CharField, SmallIntegerField

class Entity(models.Model):
    
    SP = 0
    IDP = 1
    
    entityId = CharField(max_length=1024,unique=True,editable=False)
    display_name = CharField(max_length=1024,blank=True,null=True)
    type = SmallIntegerField(blank=False,editable=False,choices=((IDP,"Identity Provider"),(SP,"Service Provider")))
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s (%s)" % (self.name(),self.type)
    
    def name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.entityId