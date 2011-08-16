'''
Created on Dec 13, 2010

@author: leifj
'''
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from coip.apps.userprofile.models import Identifier
from django_extensions.utils import uuid            
from django.contrib import auth
from django.contrib.auth.models import UNUSABLE_PASSWORD, User
import logging

def _headers(request,attr):
    v = request.META.get(attr)
    if not v:
        return None
    values = filter(lambda x: x != "(null)",v.split(";"))
    return values;

def meta1(request,attr):
    v = _headers(request,attr)
    if v:
        return v[0]
    else:
        return None

class MappedUserProxy(User):
    
    def __init__(self,user,identifier):
        self.user = user
        self.identifier = identifier
        
    def __unicode__(self):
        return self.identifier.display_name
    
    def get_full_name(self):
        return self.identifier.display_name
        
    def __getattr__(self,attr):
        if attr == 'identifier':
            return self.identifier
        return getattr(self.user,attr)

class MappedRemoteUserMiddleware(object):
    """
    Middleware for utilizing Web-server-provided authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_USER`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.

    The header used is configurable and defaults to ``REMOTE_USER``.  Subclass
    this class and change the ``header`` attribute if you need to use a
    different header.
    """

    # Name of request header to grab username from.  This will be the key as
    # used in the request.META dictionary, i.e. the normalization of headers to
    # all uppercase and the addition of "HTTP_" prefix apply.
    header = "REMOTE_USER"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        if request.user.is_authenticated():
            # this is to make internal users work too...
            if not isinstance(request.user, MappedUserProxy) and not request.user.is_anonymous():
                user = request.user
                identifier,created = Identifier.objects.get_or_create(user=user,value=user.username,type=Identifier.INTERNAL,verified=True)
                request.user = MappedUserProxy(user,identifier)
            return
        
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        
        idp = meta1(request,'Shib-Identity-Provider')
        if not idp:
            raise Exception("No IdP information in request")
        
        user = None
        identifier = None
        try:
            # Try to find a user based on the identifier received. If we find it we turn
            # around and authenticate the username as if it was received in the header.
            idp = meta1(request,'Shib-Identity-Provider')
            identifier = Identifier.objects.get(value=username,type=Identifier.FEDERATION,idp=idp,verified=True)
            user = auth.authenticate(remote_user=identifier.user.username)
        except ObjectDoesNotExist:
            pass
        
        if user == None:
            # We've never seen this identifier before. Create a new random uuid for the
            # django username and associate the identifier with it.
            user = auth.authenticate(remote_user=uuid.uuid4());
            user.password = UNUSABLE_PASSWORD
            user.save()
            identifier = Identifier.objects.create(user=user,value=username,type=Identifier.FEDERATION,idp=idp,verified=True)
            
        if not identifier:
            raise Exception("Unable to create user/id mapping")
            
        update = False
        cn = meta1(request,'cn')
        fn = meta1(request,'givenName')
        ln = meta1(request,'sn')
        
        if not cn:
            cn = meta1(request,'displayName')
        if not cn and fn and ln:    
            cn = "%s %s" % (fn,ln)    
        if not cn:
            cn = "%s according to %s" % (identifier.value,identifier.idp)
        
        if identifier.display_name != cn:
            identifier.display_name = cn
            identifier.save()    
        
        mail = meta1(request,'mail')
        if mail:
            mail_id,created = Identifier.objects.get_or_create(user=user,value=mail,type=Identifier.EMAIL,verified=True)
            user.email = mail
            update = True
            
        if fn:
            identifier.user.first_name = fn
            update = True
        if ln:
            identifier.user.last_name = ln
            update = True
            
        if update:
            identifier.user.save()
            
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = MappedUserProxy(user,identifier)
            auth.login(request, user)
            

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError: # Backend has no clean_username method.
            pass
        return username
