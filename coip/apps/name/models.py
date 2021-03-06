'''
Created on Jun 24, 2010

@author: leifj
'''
from django.db import models
import re
from pprint import pformat
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
import logging
from coip.settings import PREFIX_URL

class Attribute(models.Model):
    name = models.CharField(unique=True,max_length=255)
    description = models.TextField(blank=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name;

FMT_URN = 0
FMT_URL = 1

class Name(models.Model):
    '''
    A name-space/authorization/right/group/collaboration/thing
    '''   
    type = models.ForeignKey(Attribute, blank=True, null=True,related_name='names')
    value = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True,related_name='children')
    short = models.CharField(max_length=64,blank=True)
    creator = models.ForeignKey(User,blank=True, null=True)
    display = models.TextField(editable=False)
    description = models.TextField(blank=True)
    format = models.SmallIntegerField(default=FMT_URN,choices=((FMT_URN,"URN"),(FMT_URL,"URL")))
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    def mode(self):
        if not self.format:
            return FMT_URN
        else:
            return self.format
    
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
        return self.display
    
    def display_str(self):
        if self.mode() == FMT_URN:
            return self.display_str_urn()
        elif self.mode() == FMT_URL:
            return self.display_str_url()
        else:
            raise Exception,"unknown format for %s (%d)" % (self.value,self.id)
    
    def display_str_urn(self):
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
    
    def display_str_url(self):
        n = self
        str = ""
        while n:
            sep = ""
            av = n.relative_name()
            
            if n.parent:
                if not '=' in av:
                    sep = '/'
                else:
                    sep = ';'
                    
            str = sep+av+str
            n = n.parent
        
        return str
    
    def url(self):
        return "%s/name/%s" % (PREFIX_URL,self.display_str_url())
    
    def uri(self):
        if self.mode() == FMT_URN:
            return self.display
        else: # implement more format as needed
            return "%s/name/%s" % (PREFIX_URL,self.display)
        
    def summary(self):
        return {'name': self.display, 'url': self.url(), 'short': self.short}
    
    def remove(self,recursive=False):
        if recursive:
            for c in self.children.all():
                c.remove(recursive)
        self.delete()
    
    def copyacl(self,name):
        found_ace = False
        for ace in name.lspacl():
            found_ace = True
            self.setacl(ace.dst,ace.data)
            
        if not found_ace:
            for ace in name.lsacl():
                self.setacl(ace.dst,ace.data)
            
    def link(self,dst,type,data):
        if not self.has_link(dst,NameLink.part_of,data):
            link = NameLink(src=self,dst=dst,type=type,data=data)
            link.save()

    def unlink(self,dst,type,data):
        try:
            link = NameLink.objects.get(src=self,dst=dst,type=type,data=data)
            link.delete()
        except ObjectDoesNotExist:
            pass

    def has_link(self,dst,type,data):
        return NameLink.objects.filter(src=self,dst=dst,type=type,data=data).count() > 0

    def setacl(self,name,perm,type=0):
        (link,created) = NameLink.objects.get_or_create(src=self,dst=name,type=type)
        if not (link.data and link.data == perm):
            link.data = perm
            link.save()
            
    def setpacl(self,name,perm):
        return self.setacl(name, perm, NameLink.access_control_policy)
        
    def rmacl(self,name,perm,type=0):
        try:
            link = NameLink.objects.get(src=self,dst=name,type=type)
            save = False
            for p in perm:
                link.data = link.data.replace(p,'')
                save = True
            if save:
                if link.data:
                    link.save()
                else:
                    link.delete()
        except ObjectDoesNotExist:
            pass
        
    def rmpacl(self,name,perm):
        return self.rmacl(name,perm,NameLink.access_control_policy)
       
    def lspacl(self):
        return self.lsacl(NameLink.access_control_policy)
    
    def lsacl(self,type=0):
        return NameLink.objects.filter(src=self,type=type)
        
    def add_partof(self,part):
        self.link(part,NameLink.part_of,None)
    
    def has_permission(self,user,perm):
        logging.warn(pformat([self,user,perm]))
        #pprint("has_permission %s %s %s" % (self,user,perm))
        # TODO: reverse order of test for production system - will spead-up superuser-test and it is cheap
        logging.warn(NameLink.objects.filter(src=self,type=NameLink.access_control,data=perm,dst__memberships__user=user))
        # user is superuser or acl is on implicit group or user is member of acl group
        anyuser = lookup("system:anyuser",True)
        if NameLink.objects.filter(src=self,dst=anyuser,type=NameLink.access_control,data__contains=perm).count() > 0:
            return True
        if NameLink.objects.filter(src=self,type=NameLink.access_control,data__contains=perm,dst__memberships__user=user).count() > 0:
            return True
        
        #if user.is_superuser:
        #    return True
        
        return False #user.is_superuser
    
    def permitted_children(self,user,perm):
        return filter(lambda s: s.has_permission(user,perm),self.children.all())
    
def set_display(sender,**kwargs):
    kwargs['instance'].display = kwargs['instance'].display_str()
    
pre_save.connect(set_display,sender=Name)
    
class NameLink(models.Model):
    src = models.ForeignKey(Name,related_name='sources')
    dst = models.ForeignKey(Name,related_name='destinations')
    type = models.IntegerField()
    data = models.CharField(max_length=255,blank=True,null=True)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    
    access_control = 0
    part_of = 1
    access_control_policy = 2
    
    def __unicode__(self):
        return "%s -> %s [%s %s]" % (self.src,self.dst,self.type,self.data)
    
def roots():
    return Name.objects.filter(parent=None)
    
def _traverse(name,callable,user,depth):
    if not name:
        return [_traverse(s,callable,user,depth - 1) for s in roots()]
    else:
        t = callable(name,depth)
        if depth > 0:
            children = [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'l')]
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
                children = [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'l')]
                if children:
                    t['children'] = children
            return t
        else:
            return [_traverse(s,callable,user,depth - 1) for s in name.permitted_children(user,'l')]

    
# TODO - remove system user dependency
def walkto(root,nameparts,autocreate=False):
    name = None
    for n in nameparts:
        (a,eq,v) = n.partition('=')
        #pprint("walkto %s -> %s" % (root,n))
        if v:
            attribute = Attribute.objects.get(name=a)
            try:
                name = Name.objects.get(parent=root,type=attribute.id,value=v)
            except ObjectDoesNotExist,e:
                if autocreate:
                    name = Name(parent=root,creator=None,type=attribute.id,value=v)
                    name.save()
                    if root:
                        name.copyacl(root)
                    
                else:
                    raise e
        else:
            try:
                name = Name.objects.get(parent=root,type=None,value=a)
            except ObjectDoesNotExist,e:
                if autocreate:
                    name = Name(parent=root,creator=None,type=None,value=a)
                    name.save()
                    if root:
                        name.copyacl(root)
                else:
                    raise e
        root = name
    return name

def lookup(name,autocreate=False):
    return walkto(None,nameparts=re.compile('[\/;:]').split(name),autocreate=autocreate)

def attribute(a):
    Attribute.objects.get_or_create(name=a)
