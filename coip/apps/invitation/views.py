'''
Created on Jun 23, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from apps.invitation.forms import InvitationForm
from apps.invitation.models import Invitation
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

@login_required
def create(request):
    user = request.user
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data["to"]
            expires = form.cleaned_data["expires"]
            invitation = Invitation(sender=user,to=to,expires=expires)
            invitation.save()
            invitation.send_email()
            return HttpResponseRedirect("/user/home")
    else:
        form = InvitationForm({});
    
    return render_to_response('apps/invitation/create.html')

def accept(request,token):
    user = request.user
    invitation = Invitation.objects.get(token=token)
    
        