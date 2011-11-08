'''
Created on Nov 8, 2011

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.name.models import Name
from coip.multiresponse import json_response, render403
from django_oauth2_lite.decorators import oauth2_required
from actstream.models import Action
from django.http import HttpResponseNotFound
from coip.extensions.templatetags.userdisplay import userdisplay
import socket

def domain():
    return socket.getfqdn(socket.gethostname())

def user_to_json(o):
    return {
        'objectType': 'person',
        'id': "%s:%s" % (domain(),o.username),
        'displayName': userdisplay(o)
    }

def name_to_json(o):
    return {
         'objectType': 'group',
         'id': "%s:%d" % (domain(),o.id),
         'url': o.url(),
         'displayName': o.shortname()
    }

def object_to_json(o):
    if o:
        n = o.__class__.__name__
        if n == 'User':
            return user_to_json(o)
        if n == 'Name':
            return name_to_json(o)
    else:
        return "none"

def activity_to_json(activity):
    r = {
        "published": activity.timestamp.isoformat(),
        "actor": object_to_json(activity.actor),
        "verb": activity.verb,
        "object": object_to_json(activity.action_object),
        "target": object_to_json(activity.target)
     }
    return r

def collection_to_json(lst):
    return {
            'totalItems': len(lst),
            'items': lst
    }

@oauth2_required(scope='memberships')
def name(request,id):
    name = get_object_or_404(Name,pk=id)
    if not name.has_permission(request.user,'r'):
        return render403(request,"You do not have permission to view membership information for %s" % (name))
    # check ownership
    stream = Action.objects.stream_for_object_as_target(name)
    if stream:
        return json_response(collection_to_json([activity_to_json(activity) for activity in stream]))
    else:
        return HttpResponseNotFound()