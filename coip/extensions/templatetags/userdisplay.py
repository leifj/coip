from django import template
 
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
    return userdisplay(membership.user)
    
memberdisplay.is_safe = True
register.filter(memberdisplay)