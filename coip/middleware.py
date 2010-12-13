'''
Created on Dec 13, 2010

@author: leifj
'''
from django.core.exceptions import ImproperlyConfigured
from coip.apps.userprofile.models import UserProfile

class UserMappingMiddleware(object):
    '''
    Middleware for supporting merged and mapped user identities
    '''

    def process_request(self,request):
        if not hasattr(request,'user'):
            raise ImproperlyConfigured("Place before RemoteUserMiddleware")
        
        username = request.META['REMOTE_USER']
        qs = UserProfile.objects.filter(user__username=username,primary=True)
        if qs:
            profile = qs[0]
            username = profile.identifier

        request.META['REMOTE_USER'] = username
            
            