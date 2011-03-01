'''
Created on Jun 23, 2010

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.membership.models import Membership, add_member, remove_member
from coip.multiresponse import render403, respond_to
from django.contrib.auth.models import User
from coip.apps.name.models import Name
from django.http import HttpResponseRedirect

def show(request,id):
    membership = get_object_or_404(Membership,pk=id)
    name = membership.name
    if not name.has_permission(request.user,'r'):
        return render403("You do not have permission to view membership information for %s" % (name))
    
    return respond_to(request,{'text/html': 'apps/membership/membership.html'}, 
                      {'membership': membership,
                       'render': {'edit': name.has_permission(request.user,'w'),
                                  'delete': name.has_permission(request.user,'d'),
                                  'disable': name.has_permission(request.user,'d')}})
    
def join(request,id,member=None):
    name = get_object_or_404(Name,pk=id)
    user = request.user
    if member:
        user = User.objects.get(username=member)
    add_member(name, user)
    return HttpResponseRedirect(name.url())

def leave(request,id,member=None):
    name = get_object_or_404(Name,pk=id)
    user = request.user
    if member:
        user = User.objects.get(username=member)
    remove_member(name, user)
    return HttpResponseRedirect(name.url())