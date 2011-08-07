'''
Created on Jul 6, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.userprofile.models import PKey
from django.http import HttpResponseRedirect
from coip.multiresponse import respond_to, json_response
from coip.apps.membership.models import Membership, add_member
from coip.apps.userprofile.utils import user_profile
from django.core.exceptions import ObjectDoesNotExist
from pprint import pformat
from coip.apps.auth.utils import nonce
from coip.apps.name.models import Name, NameLink, lookup
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@login_required
def merge(request,pkey=None):
    if pkey:
        profile = user_profile(request)
        merge_profile,pkey = profile(request,pkey)
        if merge_profile:  
            merge_profile.user.delete()
            merge_profile.user = request.user
            merge_profile.save()
            pkey.delete()
        return HttpResponseRedirect("/user/home")
    else:
        profile = profile(request)
        k = PKey(profile=profile,key=nonce())
        k.save()
        return HttpResponseRedirect("/accounts/login?next=/user/merge/"+k.key)
    
@login_required
def home(request):
    memberships = []
    try:
        memberships = Membership.objects.filter(user=request.user,hidden=False)
    except ObjectDoesNotExist:
        pass
    
    urn = lookup("urn",True)
    anyuser = lookup("system:anyuser",True)
    urn.setacl(anyuser,'rl')
    
    profile = user_profile(request)
    home = lookup('user:'+request.user.username,autocreate=True)
    home.short = "%s (%s)" % (profile.display_name,profile.identifier)
    profile.home = home
    home.save()
    add_member(home,profile.user,hidden=True)
    home.setacl(home,"rwlda") #don't allow users to delete or reset acls on their home, nor invite members - that would be confusing as hell
    
    names = [(link.src,link.data) for link in NameLink.objects.filter(dst__memberships__user=request.user,type=NameLink.access_control,data__contains='i').all()]
    
    return respond_to(request, {'text/html': 'apps/userprofile/home.html'},{'memberships': memberships,'names': names})

@login_required
def search(request):
    list = []
    if request.REQUEST.has_key('term'):
        term = request.REQUEST['term']
        list = [{'label': user.username,'value': user.id} for user in User.objects.filter(username__contains=term)]
    return json_response(list)

@login_required
def info(request,username):
    user = get_object_or_404(User,username=username)
    return json_response({'username': user.username}); 