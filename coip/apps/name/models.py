'''
Created on Jun 24, 2010

@author: leifj
'''
from django.db import models
from django.contrib.auth.models import User
import re

class Attribute(models.Model):
    name = models.CharField(unique=True,max_length=255)
    description = models.TextField(blank=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name;

class Name(models.Model):
    '''
    A name-space/authorization/right/group/collaboration/thing
    '''
    type = models.ForeignKey(Attribute, blank=True, null=True,related_name='names')
    value = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True,related_name='children')
    partof = models.ForeignKey('self', blank=True, null=True,related_name='parts')
    acl = models.TextField(blank=True) # fully-qualified-name '#' rights
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def relative_name(self):
        if self.type:
            return "%s=%s" % (self.type.name,self.value)
        else:
            return self.value
    
    def __unicode__(self):
        n = self
        str = ""
        while n:
            sep = ""
            av = n.relative_name()
            
            if n.parent:
                if av.find("=") == -1:
                    sep = ':'
                else:
                    sep = ';'
                    
            str = sep+av+str
            n = n.parent
        
        return str
    
def walkto(root,nameparts):
    name = None
    for n in nameparts:
        (a,eq,v) = n.partition('=')
        if v:
            attribute = Attribute.objects.get(name=a)
            name = Name.objects.get(parent=root,type=attribute.id,value=v)
        else:
            name = Name.objects.get(parent=root,type=None,value=a)
    return name

def lookup(name):
    return walkto(None,nameparts=re.compile('[;:]').split(name))

def attribute(a):
    Attribute.objects.get_or_create(name=a)
    