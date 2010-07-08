'''
Created on Jun 24, 2010

@author: leifj
'''
from django.db import models
import re
from twisted.python.reflect import ObjectNotFound
from pprint import pprint

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
    short = models.CharField(max_length=64,blank=True)
    description = models.TextField(blank=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def shortname(self):
        if self.short:
            return self.short
        else:
            return self.__unicode__()
    
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
    
    def has_permission(self,user,perm):
        return True
    
    def permitted_children(self,user,perm):
        return filter(lambda s: s.has_permission(user,perm),self.children.all())
    
def roots():
    return Name.objects.filter(parent=None)
    
def _traverse(name,callable,user,depth):
    if not name:
        return [_traverse(s,callable,user,depth - 1) for s in roots()]
    else:
        t = callable(name,depth)
        if depth > 0:
            children = [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'#l')]
            if children:
                t['children'] = children 
        return t
    
def traverse(name,callable,user,depth,includeroot=False):
    if not name:
        return [_traverse(s,callable,user,depth - 1) for s in roots()]
    else:
        if includeroot:
            t = callable(name,depth)
            if depth > 0:
                children = [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'#l')]
                if children:
                    t['children'] = children
            return t
        else:
            return [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'#l')]
    
def walkto(root,nameparts,autocreate=False,autoacl='#l'):
    name = None
    for n in nameparts:
        (a,eq,v) = n.partition('=')
        if v:
            attribute = Attribute.objects.get(name=a)
            try:
                name = Name.objects.get(parent=root,type=attribute.id,value=v)
            except ObjectNotFound,e:
                if autocreate:
                    name = Name.objects.create(parent=root,type=attribute.id,value=v,acl=autoacl)
                else:
                    raise e
        else:
            try:
                name = Name.objects.get(parent=root,type=None,value=a)
            except ObjectNotFound,e:
                if autocreate:
                    name = Name.objects.create(parent=root,type=None,value=a,acl=autoacl)
                else:
                    raise e
    return name

def lookup(name,autocreate=False,autoacl='#l'):
    return walkto(None,nameparts=re.compile('[;:]').split(name),autocreate=autocreate,autoacl=autoacl)

def attribute(a):
    Attribute.objects.get_or_create(name=a)
    