'''
Created on Jul 5, 2010

@author: leifj
'''
from django.http import HttpResponseRedirect
from coip.apps.userprofile.models import UserProfile
from django.contrib.auth.models import User
from uuid import uuid4

def meta(request,attr):
    v = request.META.get(attr)
    values = v.split(";")
    return values[0]

def accounts_login_federated(request):
    if request.user.is_authenticated():
        profile = UserProfile.objects.get_or_create(identifier=request.user.username)
        if profile.user:
            request.user = profile.user
        else:
            profile.identifier = request.user.username
            request.user = User(username=uuid4().urn)
            request.user.save()
            profile.user = request.user
            
        update = False
        cn = meta(request,'HTTP_CN')
        if not cn:
            cn = meta(request,'HTTP_DISPLAYNAME')
        if not cn:
            fn = meta(request,'HTTP_GIVENNAME')
            ln = meta(request,'HTTP_SN')
            cn = "%s %s" % (fn,ln)
        if not cn:
            cn = profile.identifier
            
        mail = meta(request,'HTTP_MAIL')
        
        for attrib_name, meta_value in (('display_name',cn),('email',mail)):
            attrib_value = getattr(profile, attrib_name)
            if meta_value and not attrib_value:
                setattr(profile,attrib_name,meta_value)
                update = True
                
        if request.user.password == "":
            request.user.password = "(not used for federated logins)"
            update = True
            
        if update:
            request.user.save()
            profile.save()
        next = request.session.get("after_login_redirect", None)
        if next is not None:
            return HttpResponseRedirect(next)
    else:
        pass
    return HttpResponseRedirect("/")

def logout(request):
    from django.contrib.auth import logout
    logout(request) 
    return HttpResponseRedirect("/Shibboleth.sso/Logout")