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
         'l':'list members'} 

def permdisplay(perm):
    if perm:
        return "can %s" % (', '.join([perms[p] for p in perm]))
    else:
        return "can do nothing"
    
permdisplay.is_safe = True
register.filter(permdisplay)    

def acldstdisplay(dst):
    if dst.display.startswith("user:"):
        (pfx,username) = split(dst.display,":",1)
        user = User.objects.get(username=username)
        if user:
            return userdisplay(user)
        else:
            return "Unknown user \"%s\"" % username
    else:
        return "Members of <a tip=\"%s\" href=\"/name/%d\">%s</a>" % (dst.display,dst.id,dst.short)
    

acldstdisplay.is_safe = True
register.filter(acldstdisplay)