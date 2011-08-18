'''
Created on Jul 6, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to, json_response
from coip.apps.membership.models import Membership
from django.core.exceptions import ObjectDoesNotExist
from coip.apps.name.models import NameLink
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@login_required
def home(request):
    memberships = []
    try:
        memberships = Membership.objects.filter(user=request.user,hidden=False)
    except ObjectDoesNotExist:
        pass
    
    names = [(link.src,link.data) for link in NameLink.objects.filter(dst__memberships__user=request.user,type=NameLink.access_control,data__contains='i').all()]
    
    return respond_to(request, {'text/html': 'apps/userprofile/home.html'},{'memberships': memberships,'names': names})

@login_required
def search(request):
    list = []
    if request.REQUEST.has_key('term'):
        term = request.REQUEST['term']
        list = [{'label': user.username,'value': user.id} for user in User.objects.filter(username__contains=term)]
    return json_response(list)

@login_required
def info(request,username):
    user = get_object_or_404(User,username=username)
    return json_response({'username': user.username}); 