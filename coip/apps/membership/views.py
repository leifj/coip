'''
Created on Jun 23, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.membership.models import Membership
from coip.apps.membership.forms import InvitationForm
from django.http import HttpResponseRedirect
from coip.apps.auth.utils import nonce
from coip.multiresponse import respond_to

#@login_required
#def memberships(request,name):
#    
#    Membership.objects.get(name)
    
    
@login_required
def invite(request):
    user = request.user
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            expires = form.cleaned_data["expires"]
            message = form.cleaned_data["message"]
            membership = Membership(inviter=user,email=email,message=message,expires=expires,nonce=nonce())
            membership.save()
            membership.send_email()
            return HttpResponseRedirect("/membership/id/"+membership.id)
    else:
        form = InvitationForm({});
    
    return respond_to(request,{'text/html': 'apps/invitation/create.html'},{'form': form})

def accept(request,nonce):
    user = request.user
    membership = Membership.objects.get(nonce=nonce)