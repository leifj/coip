'''
Created on Jul 5, 2010

@author: leifj
'''
from django.http import HttpResponseRedirect
from coip.apps.userprofile.models import UserProfile
from django.contrib.auth.models import User
from coip.apps.auth.utils import anonid
from coip.apps.name.models import lookup
import datetime
from django.views.decorators.cache import never_cache
import logging

def meta(request,attr):
    v = request.META.get(attr)
    if not v:
        return None
    values = filter(lambda x: x != "(null)",v.split(";"))
    return values;

def meta1(request,attr):
    v = meta(request,attr)
    if v:
        return v[0]
    else:
        return None

def accounts_login_federated(request):
    if request.user.is_authenticated():
        profile,created = UserProfile.objects.get_or_create(identifier=request.META.get("REMOTE_USER"))
        if created:
            profile.identifier = request.user.username
            request.user.delete()
            request.user = User(username=anonid())
            request.user.save()
            profile.user = request.user
        else:
            request.user.delete()
            request.user = profile.user
            update = True
            
        
        update = False
        cn = meta1(request,'cn')
        if not cn:
            cn = meta1(request,'displayName')
        logging.warn(cn)
        if not cn:
            fn = meta1(request,'givenName')
            ln = meta1(request,'sn')
            if fn and ln:
                cn = "%s %s" % (fn,ln)
        if not cn:
            cn = profile.identifier
            
        mail = meta1(request,'mail')
        
        idp = meta1(request,'Shib-Identity-Provider')
        
        for attrib_name, meta_value in (('display_name',cn),('email',mail),('idp',idp)):
            attrib_value = getattr(profile, attrib_name)
            if meta_value and not attrib_value:
                setattr(profile,attrib_name,meta_value)
                update = True
                
        if request.user.password == "":
            request.user.password = "(not used for federated logins)"
            update = True
            
        if update:
            request.user.save()
        
        # Allow auto_now to kick in for the lastupdated field
        #profile.lastupdated = datetime.datetime.now()    
        profile.save()
            
        next = request.session.get("after_login_redirect", None)
        if next is not None:
            return HttpResponseRedirect(next)
    else:
        pass
    return HttpResponseRedirect("/")

@never_cache
def logout(request):
    from django.contrib.auth import logout
    logout(request) 
    return HttpResponseRedirect("/Shibboleth.sso/Logout")