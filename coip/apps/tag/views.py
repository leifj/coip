'''
Created on Mar 3, 2011

@author: jbn
'''
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to, json_response, render403
import logging
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from coip.apps.membership.models import Membership
from tagging.models import Tag

def modify(request, type, id):
    if type == "membership":
        tagobj = get_object_or_404(Membership, pk=id)
        name = tagobj.name
        tagtype = "roles"
    else: 
        return HttpResponseNotFound()
    
    if not name.has_permission(request.user,'w'):
        return render403("You do not have permission to modify roles on members of %s" % (name))
    
    if request.method == 'POST':
        to_tags = request.POST.getlist('tags[]')
        Tag.objects.update_tags(tagobj,' '.join(to_tags))
        return HttpResponseRedirect(name.url())
    
    return respond_to(request,{'text/html': 'apps/tag/modify.html'},{'tagobj': tagobj, 'tagtype': tagtype, 'type': type, 'name': tagobj.name})