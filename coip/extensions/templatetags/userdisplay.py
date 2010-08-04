from django import template
from django.template import defaultfilters
from coip.apps.userprofile.models import last_used_profile
from pprint import pprint
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
def userdisplay(user):
    try:
        p = last_used_profile(user)
        return p.display_name
    except Exception,e:
        pprint(e)
        return user.username

userdisplay.is_safe = True
register.filter(userdisplay)

def lastidentifier(user):
    #try:
        p = last_used_profile(user)
        return p.identifier
    #except Exception,e:
    #    pprint(e)
    #    return user.username

lastidentifier.is_safe = True
register.filter(lastidentifier)