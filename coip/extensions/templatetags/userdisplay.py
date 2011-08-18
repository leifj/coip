from django import template
from pprint import pformat
import logging
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
def userdisplay(user):
    if user == None:
        return "anonymous"
    profile = user.get_profile()
    if profile and profile.display_name:
        return profile.display_name
    cn = user.get_full_name()
    if cn:
        return cn
    else:
        return user.username

userdisplay.is_safe = True
register.filter(userdisplay)

def memberdisplay(membership):
    if membership.user:
        return userdisplay(membership.user)
    else:
        return membership.entity.display_name
    
memberdisplay.is_safe = True
register.filter(memberdisplay)