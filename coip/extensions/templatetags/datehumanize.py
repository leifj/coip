from django import template
from django.template import defaultfilters
 
register = template.Library()
 
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
def datehumanize(value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    """
 
    from datetime import datetime
 
    if isinstance(value, datetime):
        delta = datetime.now() - value
        if delta.days > 6:
            return value.strftime("on %b %d")                    # May 15
        if delta.days > 1:
            return value.strftime("on %A")                       # Wednesday
        elif delta.days == 1:
            return 'yesterday'                                # yesterday
        elif delta.seconds > 3600:
            return str(delta.seconds / 3600 ) + ' hours ago'  # 3 hours ago
        elif delta.seconds >  MOMENT:
            return str(delta.seconds/60) + ' minutes ago'     # 29 minutes ago
        else:
            return 'a moment ago'                             # a moment ago
        return defaultfilters.date(value)
    else:
        return str(value)
datehumanize.is_safe = True
register.filter(datehumanize)