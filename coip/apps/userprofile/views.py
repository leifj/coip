'''
Created on Jul 6, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.userprofile.models import PKey
from django.http import HttpResponseRedirect
from uuid import uuid4
from coip.multiresponse import respond_to
from coip.apps.membership.models import Membership
from coip.apps.userprofile.utils import user_profile
from django.core.exceptions import ObjectDoesNotExist
from pprint import pprint

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
        k = PKey(profile=profile,key=uuid4().hex)
        k.save()
        return HttpResponseRedirect("/accounts/login?next=/user/merge/"+k.key)
    
@login_required
def home(request):
    memberships = []
    try:
        memberships = Membership.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        pass
    
    pprint(memberships)
    return respond_to(request, {'text/html': 'apps/userprofile/home.html'},{'memberships': memberships})


