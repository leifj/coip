'''
Created on Jul 5, 2010

@author: leifj
'''
from django.http import HttpResponseRedirect
from coip.apps.userprofile.views import home_name
from django.views.decorators.cache import never_cache

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
        user = request.user
        profile = user.get_profile()
        profile.identifier = request.user.username
        idp = meta1(request,'Shib-Identity-Provider')
        profile.idp = idp
        
        cn = meta1(request,'cn')
        fn = meta1(request,'givenName')
        ln = meta1(request,'sn')
        mail = meta1(request,'mail')
        
        if not cn:
            cn = meta1(request,'displayName')
        if not cn and (fn and ln):
            cn = "%s %s" % (fn,ln)
        if not cn:
            cn = profile.identifier

        if fn:
            user.first_name = fn
        if ln:
            user.last_name = ln
        if mail:
            user.email = mail
            
        if cn:
            profile.display_name = cn
                
        user.set_unusable_password()
        
        if profile.home == None:
            profile.home = home_name(user,autocreate=True)
        
        profile.home.short = "%s (%s)" % (cn,profile.identifier)
        profile.home.save()
        user.save()
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