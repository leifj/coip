from django import template
from coip.extensions.templatetags.userdisplay import userdisplay
from string import split
from django.contrib.auth.models import User
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
perms = {'r':'read',
         'w':'write',
         'd':'delete',
         'i':'manage members',
         'l':'list members',
         'a':'manage rights'} 

def permdisplay(perm):
    if perm:
        return "can %s" % (', '.join([perms[p] for p in perm]))
    else:
        return "can do nothing"
    
permdisplay.is_safe = True
register.filter(permdisplay)    

def acldstdisplay(dst):
    if dst.display.startswith("user:") and dst.display.count(":") == 1:
        (pfx,username) = split(dst.display,":",1)
        user = User.objects.get(username=username)
        if user:
            return userdisplay(user)
        else:
            return "Unknown user \"%s\"" % username
    elif dst.display == 'system:anyusers':
        return "All users"
    elif dst.display == 'system:anyentity':
        return "All services and identity providers"
    elif dst.display == 'system:anysp':
        return "All services"
    elif dst.display == 'system:anyidp':
        return "All identity providers"
    else:
        return "members of %s (%s)" % (dst.short,dst.display)
    

acldstdisplay.is_safe = True
register.filter(acldstdisplay)