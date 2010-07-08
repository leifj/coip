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
from coip.apps.name.forms import NameEditForm
from twisted.python.reflect import ObjectNotFound

def edit(request,id):
    name = None
    try:
        name = Name.objects.get(id=id)
    except ObjectNotFound:
        return HttpResponseNotFound()
    
    if not name.has_permission(request.user,'#w'):
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        form = NameEditForm(request.POST,instance=name)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/name/id/%d" % name.id)
    else:
        form = NameEditForm(instance=name)
        
    return respond_to(request,{'text/html': 'apps/name/edit.html'},{'form': form,'name': name})
            

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
                          {'name': name, 'memberships': name.memberships, 'edit': name.has_permission(request.user,'#w')})
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