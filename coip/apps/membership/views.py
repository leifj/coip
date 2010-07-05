'''
Created on Jun 23, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.membership.models import Membership

@login_required
def memberships(request,name):
    
    Membership.objects.get(name)
    