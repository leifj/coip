'''
Created on Nov 8, 2011

@author: leifj
'''
import re
from django.contrib.auth.models import User
from coip.multiresponse import json_response
from coip.apps.activitystreams.views import object_to_json
from django_oauth2_lite.decorators import oauth2_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from coip.apps.name.models import Name
from django.utils import simplejson

def _resolve_user(request,uid):
    if uid == '@me':
        return request.user
    
    if re.match('^[0-9]+$',uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            return None
    
    try:
        return User.objects.get(username=uid)
    except User.DoesNotExist:
        return None
    
def _resolve_group(request,user,gid):
    if gid == '@self':
        return user.get_profile().home
    
    if re.match('^[0-9]+$',gid):
        try:
            return Name.objects.get(id=gid)
        except User.DoesNotExist:
            return None
    try:
        return Name.objects.get(username=gid)
    except User.DoesNotExist:
        return None   
    
    
def _opensocial_collection(lst):
    return {
        "startIndex": 0,
        "totalResults": len(lst),
        "entry": [
            object_to_json(o) for o in lst
        ]
    }

def rpc(request):
    if request.method == 'POST' and request.META['CONTENT_TYPE'] == 'application/json':
        rpc_request = simplejson.load(request)
        if rpc_request['method'] == 'system.listMethods':
            return json_response(['people.get','groups.get','system.listMethods'])
    else:
        return HttpResponseBadRequest()
    
@oauth2_required(scope='opensocial')
def person(request,uid,gid='@self'):
    user = _resolve_user(request,uid)
    
    if not user:
        return HttpResponseNotFound("No such user")
    
    name = _resolve_group(request,user,gid)
    
    if not name:
        return HttpResponseNotFound()
    
    ##TODO - implement listing people based on group memberships
    return json_response(_opensocial_collection([user]))

@oauth2_required(scope='opensocial')
def group(request,uid='@me'):
    user = _resolve_user(request,uid)
    if not user:
        return HttpResponseNotFound("No such user")
    
    memberships = user.memberships.filter(hidden=False)
    return json_response(_opensocial_collection([m.name for m in memberships]))
    
    