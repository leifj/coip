'''
Created on Jun 23, 2010

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.membership.models import Membership
from coip.multiresponse import render403, respond_to

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