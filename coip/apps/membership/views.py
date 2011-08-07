'''
Created on Jun 23, 2010

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.membership.models import Membership, add_member, remove_member
from coip.multiresponse import render403, respond_to
from django.contrib.auth.models import User
from coip.apps.name.models import Name, lookup
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from coip.apps.entity.models import Entity
from django.contrib.auth.decorators import login_required
from coip.apps.membership.forms import MembershipForm
from coip.settings import METADATA
from lxml import etree
from pprint import pprint

def show(request,id):
    membership = get_object_or_404(Membership,pk=id)
    name = membership.name
    if not name.has_permission(request.user,'r'):
        return render403(request,"You do not have permission to view membership information for %s" % (name))
    
    return respond_to(request,
                      {'text/html': 'apps/membership/membership.html'}, 
                      {'membership': membership})
    
def import_metadata():
    doc = etree.parse(METADATA)
    ns = {'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
          'xml': 'http://www.w3.org/XML/1998/namespace'}
    for e in doc.xpath("md:EntityDescriptor",namespaces=ns):
        entityId = e.get('entityID')
        display = entityId
        x = e.xpath("md:OrganizationDisplayName",namespaces=ns)
        if x:
            display = x[0]    
        
        (entity,created) = Entity.objects.get_or_create(entityId=entityId)
        save = created
        
        if created:
            entity.type = Entity.OTHER
        
        x = e.xpath("md:SPSSODescriptor",namespaces=ns)
        if x:
            type = Entity.SP
        x = e.xpath("md:IDPSSODescriptor",namespaces=ns)
        if x:
            type = Entity.IDP
            
        if type != entity.type:
            entity.type = type
            save = True
        
        if display != entity.display_name:
            entity.display_name = display
            save = True
            
        if save:
            entity.save()
            
        anyuser = lookup("system:anyuser")
        
        anyentity = lookup("system:anyentity",True)
        anyentity.setacl(anyuser, "rl")
        
        anysp = lookup("system:anysp",True)
        anysp.setacl(anyuser, "rl")
        
        anyidp = lookup("system:anyidp",True)
        anyidp.setacl(anyuser, "rl")
        
        add_member(anyentity,entity)
        if entity.type == Entity.SP:
            add_member(anysp,entity)
        if entity.type == Entity.IDP:
            add_member(anyidp,entity)
    
@login_required
def join(request,id,membername=None):
    name = get_object_or_404(Name,pk=id)
    if not name.has_permission(request.user,'i'):
        return render403(request,"You do not have permission to add members to %s" % (name))
    
    if request.method == "POST":
        m = Membership(name=name,enabled=True)
        form = MembershipForm(request.POST,instance=m)
        if form.is_valid():
            if form.cleaned_data.has_key('user'):
                add_member(name,form.cleaned_data['user'])
            elif form.cleaned_data.has_key('entity'):
                add_member(name,form.cleaned_data['entity'])
            else:
                raise Exception,"Bad form state - should not happen at all!"
            
            return HttpResponseRedirect(name.url())
        else:
            return respond_to(request,
                              {'text/html': 'apps/membership/edit.html'},
                              {'form': form,'name': name, 'formtitle': 'Add a member to %s' % name.short})
    else:
        if membername:
            try:
                member = User.objects.get(username=membername)
            except ObjectDoesNotExist:
                member = Entity.objects.get(entityId=name)
            add_member(name, member)
            return HttpResponseRedirect(name.url())
        else:
            form = MembershipForm()
            import_metadata()
            return respond_to(request,
                              {'text/html': 'apps/membership/edit.html'},
                              {'form': form,'name': name, 'formtitle': 'Add a member to %s' % name.short})

@login_required
def leave(request,id,membername=None):
    name = get_object_or_404(Name,pk=id)
    if membername:
        try:
            member = User.objects.get(username=membername)
        except ObjectDoesNotExist:
            member = Entity.objects.get(entityId=name) 
    remove_member(name, member)
    return HttpResponseRedirect(name.url())
