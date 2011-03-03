'''
Created on Jun 23, 2010

@author: leifj
'''
from django.shortcuts import get_object_or_404
from coip.apps.membership.models import Membership, add_member, remove_member
from coip.multiresponse import render403, respond_to
from django.contrib.auth.models import User
from coip.apps.name.models import Name
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from coip.apps.entity.models import Entity
from django.contrib.auth.decorators import login_required
from coip.apps.membership.forms import MembershipForm

def show(request,id):
    membership = get_object_or_404(Membership,pk=id)
    name = membership.name
    if not name.has_permission(request.user,'r'):
        return render403("You do not have permission to view membership information for %s" % (name))
    
    return respond_to(request,
                      {'text/html': 'apps/membership/membership.html'}, 
                      {'membership': membership})
    
@login_required
def join(request,id,membername=None):
    name = get_object_or_404(Name,pk=id)
    if not name.has_permission(request.user,'i'):
        return render403("You do not have permission to add members to %s" % (name))
    
    if request.method == "POST":
        m = Membership(name=name,enabled=True)
        form = MembershipForm(request.POST,instance=m)
        if form.is_valid():
            m = form.save()
            return HttpResponseRedirect(name.url())
    else:
        if membername:
            try:
                member = User.objects.get(username=membername)
            except ObjectDoesNotExist:
                member = Entity.objects.get(entityId=name)
            add_member(name, member)
            return HttpResponseRedirect(name.url())
        else:
            form = MembershipForm()
            return respond_to(request,
                              {'text/html': 'apps/membership/edit.html'},
                              {'form': form,'name': name, 'formtitle': 'Add a member to %s' % name.short})

@login_required
def leave(request,id,membername=None):
    name = get_object_or_404(Name,pk=id)
    if membername:
        try:
            member = User.objects.get(username=membername)
        except ObjectDoesNotExist:
            member = Entity.objects.get(entityId=name) 
    remove_member(name, member)
    return HttpResponseRedirect(name.url())
