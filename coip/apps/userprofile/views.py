'''
Created on Jul 6, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.userprofile.models import PKey
from django.http import HttpResponseRedirect
from coip.multiresponse import respond_to
from coip.apps.membership.models import Membership, add_member
from coip.apps.userprofile.utils import user_profile
from django.core.exceptions import ObjectDoesNotExist
from pprint import pformat
from coip.apps.auth.utils import nonce
from coip.apps.name.models import Name, NameLink, lookup

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
        memberships = Membership.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        pass
    
    anyuser = lookup("system:anyuser",True)
    profile = user_profile(request)
    home = lookup('user:'+request.user.username,autocreate=True)
    home.short = "Home of %s (%s)" % (profile.display_name,profile.identifier)
    home.save()
    add_member(home,profile.user)
    home.setacl(home,"rliwd")
    
    names = [(link.src,link.data) for link in NameLink.objects.filter(dst__memberships__user=request.user,type=NameLink.access_control).all()]
    
    return respond_to(request, {'text/html': 'apps/userprofile/home.html'},{'memberships': memberships,'names': names})


