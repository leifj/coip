'''
Created on Jul 5, 2010

@author: leifj
'''
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache


def accounts_login_federated(request):
    if request.user.is_authenticated():
        #profile,created = UserProfile.objects.get_or_create(user=request.user)
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