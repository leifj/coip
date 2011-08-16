from django import template
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
def userdisplay(user):
    cn = user.get_full_name()
    if not cn and hasattr(user,'identifier'):
        id = user.identifier
        if id:
            cn = user.identifier.value
    if not cn:
        cn = user.username
    return cn

userdisplay.is_safe = True
register.filter(userdisplay)

def memberdisplay(membership):
    if membership.user:
        return userdisplay(membership.user)
    else:
        return membership.entity.display_name
    
memberdisplay.is_safe = True
register.filter(memberdisplay)