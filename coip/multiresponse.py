import coip.mimeparse as mimeparse
import re
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseForbidden
from coip.apps.userprofile.utils import user_profile
from django.utils import simplejson
from django.template import loader
from coip.settings import PREFIX_URL
from coip.apps.membership.models import has_member

default_suffix_mapping = {"\.htm(l?)$": "text/html",
                          "\.json$": "application/json",
                          "\.rss$": "application/rss+xml",
                          "\.torrent$": "application/x-bittorrent"}

def _accept_types(request, suffix):
    for r in suffix.keys():
        p = re.compile(r)
        if p.search(request.path):
            return suffix.get(r)
    return None


def timeAsrfc822 ( theTime ) :
    import rfc822
    return rfc822 . formatdate ( rfc822 . mktime_tz ( rfc822 . parsedate_tz ( theTime . strftime ( "%a, %d %b %Y %H:%M:%S" ) ) ) )

def make_response_dict(request,d={}):
 
    if request.user.is_authenticated():
        d['user'] = request.user
        d['profile'] = user_profile(request)

    d['prefix_url'] = PREFIX_URL
    if d.has_key('name'):
        name = d['name']
        if name:
            d['render'] = {'delete': name.has_permission(request.user,'d'),
                           'edit': name.has_permission(request.user,'w'),
                           'invite': name.has_permission(request.user,'i'),
                           'kick': name.has_permission(request.user,'i'),
                           'acl': name.has_permission(request.user,'a'),
                           'add': name.has_permission(request.user,'w'),
                           'join': name.has_permission(request.user,'i') and not has_member(name,request.user),
                           'up': (name.parent and name.parent.has_permission(request.user,'r')) or not name.parent}

    return d

def json_response(data):
    r = HttpResponse(simplejson.dumps(data),content_type='application/json')
    r['Cache-Control'] = 'no-cache, must-revalidate'
    r['Pragma'] = 'no-cache'
    
    return r

def render403(request,message="You don't seem to have enough rights for what you are trying to do....",dict={}):
    dict['message'] = message
    dict['user'] = request.user
    if request.user.is_authenticated():
        dict['profile'] = user_profile(request)
    return HttpResponseForbidden(loader.render_to_string("403.html",dict))
    
def respond_to(request, template_mapping, dict={}, suffix_mapping=default_suffix_mapping):
    accept = _accept_types(request, suffix_mapping)
    if accept is None:
        accept = (request.META['HTTP_ACCEPT'].split(','))[0]
    content_type = mimeparse.best_match(template_mapping.keys(), accept)
    template = None
    if template_mapping.has_key(content_type):
        template = template_mapping[content_type]
    else:
        template = template_mapping["text/html"]
    if callable(template):
        response = template(make_response_dict(request,dict))
    elif isinstance(template, HttpResponse):
        response = template
        response['Content-Type'] = "%s; charset=%s" % (content_type, settings.DEFAULT_CHARSET)
    else:
        response = render_to_response(template,make_response_dict(request,dict))
        response['Content-Type'] = "%s; charset=%s" % (content_type, settings.DEFAULT_CHARSET)
    return response
