'''
Created on Nov 8, 2011

@author: leifj
'''
from actstream.models import ActionManager
from actstream.views import stream
from datetime import datetime


class NameActionManager(ActionManager):
    
    @stream
    def name_activities(self, name, time=None):
        if time is None:
            time = datetime.now()
        return name.actor_actions.filter(timestamp__lte = time)