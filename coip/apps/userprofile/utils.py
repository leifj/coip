'''
Created on Jul 6, 2010

@author: leifj
'''
from coip.apps.userprofile.models import UserProfile, PKey
from django.core.exceptions import ObjectDoesNotExist

def request_profile(request):
    if request.user.is_authenticated():
        if request.META.has_key('REMOTE_USER'):
            return UserProfile.objects.get(identifier=request.META['REMOTE_USER'])
        else:
            return UserProfile.objects.get(user=request.user.id)
    else:
        return None 

def user_profile(request,key=None):
    if key:
        try:
            k = PKey.objects.get(key=key)
            return k.profile,k
        except ObjectDoesNotExist:
            return None
    else:
        return request_profile(request)
        #if not request.session.has_key('_profile'):
        #    request.session['_profile'] = request_profile(request)
        #return request.session['_profile']