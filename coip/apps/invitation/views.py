'''
Created on Jun 23, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.apps.invitation.models import Invitation
from coip.apps.invitation.forms import InvitationForm
from django.http import HttpResponseRedirect
from coip.apps.auth.utils import nonce
from coip.multiresponse import respond_to, render403
from coip.apps.name.models import Name 
import datetime
from coip.apps.membership.models import Membership
from django.shortcuts import get_object_or_404
    
@login_required
def invite(request,id):
    name = get_object_or_404(Name,pk=id)
    
    if not name.has_permission(request.user,'i'):
        return render403(request,'You are not allowed to invite users to '+name)
    
    user = request.user
    if request.method == 'POST':
        invitation=Invitation(inviter=user,nonce=nonce(),name=name)
        form = InvitationForm(request.POST,instance=invitation)
        if form.is_valid():
            invitation = form.save()
            invitation.send_email()
            return HttpResponseRedirect("/name/id/%d" % (name.id))
    else:
        exp = datetime.datetime.now()+datetime.timedelta(days=1)
        invitation=Invitation(message="Please consider joining my group!",expires=exp.strftime("%Y-%m-%d"))
        form = InvitationForm(instance=invitation);
    
    return respond_to(request,{'text/html': 'apps/invitation/edit.html'},{'form': form,'name': name,'formtitle': 'Invite someone to join %s' % (name.short),'submitname': 'Invite User'})

@login_required
def accept(request,nonce):
    invitation = get_object_or_404(Invitation,nonce=nonce)
    
    (membership,created) = Membership.objects.get_or_create(user=request.user,name=invitation.name)
    if created or not membership.enabled:
        membership.enabled = True
        membership.save()
    
    invitation.delete()
    
    return HttpResponseRedirect("/membership/%d" % (membership.id))

@login_required
def cancel(request,id):
    invitation = get_object_or_404(Invitation,pk=id)
    name = invitation.name
    
    if not name.has_permission(request.user,'w'):
        return render403(request,'You are not allowed to cancel pending invitations to %s' % (name))
    
    invitation.delete()
    return HttpResponseRedirect("/name/id/%d" % (name.id))

def resend(request,id):
    invitation = get_object_or_404(Invitation,pk=id)
    name = invitation.name
    
    invitation.send_email()
    return HttpResponseRedirect("/name/id/%d" % (name.id))
    
    
