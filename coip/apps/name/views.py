'''
Created on Jul 6, 2010

@author: leifj
'''
from coip.apps.name.models import Name, lookup, traverse, NameLink
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseForbidden,\
    HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to, json_response, render403
from pprint import pformat
import logging
from coip.apps.name.forms import NameEditForm, NewNameForm, NameDeleteForm,\
    PermissionForm
from django.shortcuts import get_object_or_404

@login_required
def delete(request,id):
    name = get_object_or_404(Name,pk=id)
    
    if not name.has_permission(request.user,'d'):
        return render403()
    
    if request.method == 'POST':
        form = NameDeleteForm(request.POST)
        if form.is_valid():
            parent = name.parent
            if not form.cleaned_data['recursive'] and name.children.count() > 0:
                return HttpResponseForbidden("Will not delete non-empty node")
            
            for link in name.links.all():
                link.delete()
            
            if form.cleaned_data['recursive']:
                name.remove(True)
            else:
                name.remove(False)
            
            if parent:
                return HttpResponseRedirect("/name/id/%d" % parent.id)
            else:
                return HttpResponseRedirect("/name");
    else:
        form = NameDeleteForm()
            
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': name,'formtitle': 'Remove %s' % (name.short) ,'submitname': 'Delete'})

@login_required
def add(request,id):
    parent = get_object_or_404(Name,pk=id)
        
    if id:
        if not parent.has_permission(request.user,'w'):
            return HttpResponseForbidden('You are not allowed to create names under '+parent)
    else:
        if not request.user.admin:
            return HttpResponseForbidden('You are not allowed to create names in the root')
    
    if request.method == 'POST':
        name = Name(parent=parent,creator=request.user)
        form = NewNameForm(request.POST,instance=name)
        if form.is_valid():
            name = form.save()
            name.copyacl(name.parent)
            return HttpResponseRedirect("/name/id/%d" % name.id)
    else:
        form = NewNameForm()
        
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': parent,'formtitle': 'Add group','submitname': 'Create'})

@login_required
def edit(request,id):
    name = get_object_or_404(Name,pk=id)
    
    if not name.has_permission(request.user,'w'):
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        form = NameEditForm(request.POST,instance=name)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/name/id/%d" % name.id)
    else:
        form = NameEditForm(instance=name)
        
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': name,'formtitle': 'Change name','submitname': 'Update'})
            

@login_required
def editacl(request,id,type):
    name = get_object_or_404(Name,pk=id)
    
    if not name.has_permission(request.user,'a'):
        return render403("You do not have permission to change permissions on %s" % (name))
    
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            dstid = form.cleaned_data['dst']
            dst = get_object_or_404(Name,pk=dstid)
            p = form.cleaned_data['permissions']
            if not p:
                p = []
            perms = p.join('')
            link = NameLink.objects.get_or_create(src=name,dst=dst,type=NameLink.access_control)
            link.data = perms
            link.save()

    form = PermissionForm()
    return respond_to(request,{'text/html': 'apps/name/acls.html'},{'form': form, 'name': name, 'acl': name.lsacl(),'formtitle': 'Add Permission','submitname':'Add'})

@login_required
def links(request,id,type=NameLink.access_control):
    name = get_object_or_404(Name,pk=id)
    if not name.has_permission(request.user,'r'):
        return render403("You do not have permission to list name links from %s" % (name))
    
    links = name.links.filter(type=type).all
    return respond_to(request,{'text/html': 'apps/name/links.html',
                               'application/json': json_response(links)},
                               {'name': name, 'links': links})
    

@login_required
def removelink(request,id):
    link = get_object_or_404(NameLink,pk=id)
    name = link.src
    type = link.type
    if not name.has_permission(request.user,'w'):
        return render403("You do not have permission to remove name links from %s" % (name))
    
    link.delete()
    return HttpResponseRedirect("/name/{{name.id}}/link/{{type}}")
    
@login_required
def show_root(request):
    return respond_to(request, 
                      {'text/html': 'apps/name/name.html'}, 
                      {'name': None, 'memberships': None, 'edit': False})

def show(request,name):
    if not name:
        raise Http404()
    
    if name.has_permission(request.user,'r'):
        memberships = None
        invitations = None
        if name.has_permission(request.user,'l'):
            memberships = name.memberships
            invitations = name.invitations
        return respond_to(request, 
                          {'text/html': 'apps/name/name.html',
                           'application/json': json_response({'name': name.display, 'url': name.url(), 'short': name.short}) },
                          {'name': name,
                           'memberships':memberships,
                           'invitations':invitations})
    else:
        return render403()

@login_required
def show_by_name(request,name=None):
    if not name:
        return show_root(request)
    try:
        return show(request,lookup(name))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()   
   
@login_required
def show_by_id(request,id=None):
    if not id:
        return show_root(request)
    try:
        return show(request,Name.objects.get(id=id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

def _tree_node(name,depth):
    state = 'closed'
    return {'data': { 'title': name.relative_name(), 'attr': {'href': name.url() } },
            'state': state,
            'attr': {'id': name.id}}
    
def _tree(request,id=None,includeroot=False):
    name = None
    if id:
        name = Name.objects.get(id=id)
    depth = 3
    if request.GET.has_key('depth'):
        depth = request.GET['depth']
    t = traverse(name,_tree_node,request.user,depth,includeroot)
    logging.debug(t)
    return json_response(t)

@login_required
def rtree(request,id=None):
    return _tree(request,id,True)

@login_required
def ctree(request,id=None):
    return _tree(request,id,False)