'''
Created on Jul 6, 2010

@author: leifj
'''
from coip.apps.name.models import Name, lookup, traverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseForbidden,\
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to, json_response
from pprint import pprint
from coip.apps.name.forms import NameEditForm, NewNameForm, NameDeleteForm
from twisted.python.reflect import ObjectNotFound

def delete(request,id):
    name = None
    try:
        name = Name.objects.get(id=id)
    except ObjectNotFound:
        return HttpResponseNotFound()
    
    if not name.has_permission(request.user,'d'):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = NameDeleteForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['confirm']:
                return HttpResponseRedirect("/name/id/%d" % name.id)
                
            parent = name.parent
            if not form.cleaned_data['recursive'] and name.children.count() > 0:
                return HttpResponseForbidden("Will not delete non-empty node")
            
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
            
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': name,'formtitle': 'Remove name confirmation' ,'submitname': 'Delete'})

def add(request,id):
    parent = None
    if id:
        try:
            parent = Name.objects.get(id=id)
        except ObjectNotFound:
            return HttpResponseNotFound()
    
    if id:
        if not parent.has_permission(request.user,'i'):
            return HttpResponseForbidden('You are not allowed to create names under '+parent)
    else:
        if not request.user.admin:
            return HttpResponseForbidden('You are not allowed to create names')
    
    if request.method == 'POST':
        name = Name(parent=parent,creator=request.user,acl=parent.copy_acl())
        form = NewNameForm(request.POST,instance=name)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/name/id/%d" % name.id)
    else:
        form = NewNameForm()
        
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': parent,'formtitle': 'Create new name','submitname': 'Create'})

def edit(request,id):
    name = None
    try:
        name = Name.objects.get(id=id)
    except ObjectNotFound:
        return HttpResponseNotFound()
    
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
            

def show_root(request):
    return respond_to(request, 
                      {'text/html': 'apps/name/name.html'}, 
                      {'name': None, 'memberships': None, 'edit': False})

def show(request,name):
    if not name:
        return HttpResponseNotFound()
    
    if name.has_permission(request.user,'r'):
        return respond_to(request, 
                          {'text/html': 'apps/name/name.html'}, 
                          {'name': name, 
                           'memberships': name.memberships, 
                           'delete': name.has_permission(request.user,'d'),
                           'insert': name.has_permission(request.user,'i'),
                           'edit': name.has_permission(request.user,'w')})
    else:
        return HttpResponseForbidden()

@login_required
def show_by_name(request,n=None):
    if not n:
        return show_root(request)
    try:
        return show(request,lookup(n))
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
    return {'data': { 'title': name.relative_name(), 'attr': {'href': '/name/id/%d' % name.id} },
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
    pprint(t)
    return json_response(t)

@login_required
def rtree(request,id=None):
    return _tree(request,id,True)

@login_required
def ctree(request,id=None):
    return _tree(request,id,False)