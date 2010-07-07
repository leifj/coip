'''
Created on Jul 6, 2010

@author: leifj
'''
from coip.apps.name.models import Name, lookup
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to
from coip.apps.auth.authz import has_permission

def show(request,name):
    if not name:
        return HttpResponseNotFound()
    
    if has_permission(request.user,name,'r'):
        memberships = []
        if has_permission(request.user,name,'l'):
            memberships = name.memberships
        return respond_to(request, {'text/html': 'apps/name/name.html'}, {'name': name, 'memberships': memberships})
    else:
        return HttpResponseForbidden()

@login_required
def show_by_name(request,n):
    try:
        return show(request,lookup(n))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()    
   
@login_required
def show_by_id(request,id):
    try:
        return show(request,Name.objects.get(id=id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound() 