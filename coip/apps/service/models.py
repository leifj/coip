'''
Created on Feb 23, 2011

@author: leifj
'''

from django.db import models
import re
from pprint import pformat
import logging
from django.db.models.fields import CharField

class Service(models.Model):
    entityId = CharField(max_length=1024,unique=True,editable=False)
    display_name = CharField(max_length=1024,blank=True,null=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.entityId