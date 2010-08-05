'''
Created on Aug 4, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from coip.apps.name.models import Name
from coip.multiresponse import render403, respond_to
from coip.apps.link.models import Link
from coip.apps.link.forms import AddRelatedLinkForm
from django.http import HttpResponseRedirect

@login_required
def add(request,id):
    name = get_object_or_404(Name,pk=id)
    if not name.has_permission(request.user,'w'):
        return render403("You do not have permission to add a link on %s" % (name))
    
    if request.method == 'POST':
        link = Link(tag='related',name=name)
        form = AddRelatedLinkForm(request.POST,instance=link)
        if form.is_valid():
            link = form.save()
            return HttpResponseRedirect("/name/id/%d" % name.id)
    else:
        form = AddRelatedLinkForm()
        
    return respond_to(request,{'text/html': 'apps/link/edit.html'},{'form': form,'name': name,'formtitle': 'Add link','submitname': 'Add link'})

@login_required
def remove(request,id):
    link = get_object_or_404(Link,pk=id)
    name = link.name
    if not name.has_permission(request.user,'w'):
        return render403("You do not have permission to remove a link on %s" % (name))
    
    link.delete()
    
    return HttpResponseRedirect("/name/id/%d" % name.id)