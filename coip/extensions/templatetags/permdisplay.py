from django import template
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
perms = {'r':'read',
         'w':'write',
         'd':'delete',
         'i':'insert',
         'l':'list'} 

def permdisplay(perm):
    if perm:
        return "can %s" % (' '.join([perms[p] for p in perm]))
    else:
        return "can do nothing"

permdisplay.is_safe = True
register.filter(permdisplay)