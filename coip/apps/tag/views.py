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
from forms import *
from tagging.models import Tag

def add(request, type, id):
    if type == "membership":
        tagobj = get_object_or_404(Membership, pk=id)
    else: return HttpResponseNotFound()
    if request.method == 'POST':
        if tagobj.user == request.user:
            for tag in request.POST.getlist('item[tags][]'):
                Tag.objects.add_tag(tagobj, tag)
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return respond_to(request,{'text/html': 'apps/tag/add.html'},{'tagobj': tagobj, 'type': type, 'name': tagobj.name})