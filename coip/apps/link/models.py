'''
Created on Aug 4, 2010

@author: leifj
'''
from django.db import models
from coip.apps.name.models import Name

class Link(models.Model):
    name = models.ForeignKey(Name,related_name='links')
    url = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s:%s (%s) on %s" % (self.tag,self.url,self.text,self.name)