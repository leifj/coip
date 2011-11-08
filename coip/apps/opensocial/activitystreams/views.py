'''
Created on Nov 8, 2011

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.name.models import Name
from coip.multiresponse import json_response

@oauth2_required(scope='memberships')
def name(request,id):
    name = get_object_or_404(Name,pk=id)
    # check ownership
    return json_response(name.actor_actions.name_activities())