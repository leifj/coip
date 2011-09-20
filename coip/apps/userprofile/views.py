'''
Created on Jul 6, 2010

@author: leifj
'''
from django.contrib.auth.decorators import login_required
from coip.multiresponse import respond_to, json_response, render403
from coip.apps.membership.models import Membership, add_member
from django.core.exceptions import ObjectDoesNotExist
from coip.apps.name.models import NameLink, lookup, Name
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from coip.apps.userprofile.models import UserProfile
from django.db.models import Q 
from coip.extensions.templatetags.userdisplay import userdisplay
import subprocess
import re
from tempfile import NamedTemporaryFile
from coip.apps.userprofile.forms import AddSSHKeyForm, AddCertificateForm
from django.http import HttpResponseRedirect

def _add_sshkey(name,keyfile):
    p = subprocess.Popen(['ssh-keygen','-l','-f',keyfile.name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out,err) = p.communicate()
    code = p.wait()
    if code != 0:
        raise Exception("Unable to fingerprint ssh key: %d - %s" % (code,err))
    parts = out.split()
    fp = re.sub(':','',parts[1])
    
    p = subprocess.Popen(['ssh-keygen','-e','-f',keyfile.name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out,err) = p.communicate()
    code = p.wait()
    if code != 0:
        raise Exception("Unable to import ssh key: %d - %s" % (code,err))
    id = out
    
    username = "sshkey:%s" % fp
    user,created = User.objects.get_or_create(username=username)
    profile = user.get_profile()
    if created:
        profile.type = UserProfile.SSHKEY
        profile.home = name
        profile.display = "SSH Key (%s)" % (fp)
        profile.identifier = id
        
        add_member(profile.home,user)
        profile.save()
        
        
def _add_gridcert(name,keyfile):
    p = subprocess.Popen(['openssl','x509','-noout','-fingerprint','-sha1','-in',keyfile.name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out,err) = p.communicate()
    code = p.wait()
    if code != 0:
        raise Exception("Unable to fingerprint X509 certificate: %d - %s" % (code,err))
    parts = out.split('=')
    fp = re.sub(':','',parts[1].lower())
    
    p = subprocess.Popen(['openssl','x509','-outform','PEM','-in',keyfile.name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (out,err) = p.communicate()
    code = p.wait()
    if code != 0:
        raise Exception("Unable to import X509 certificate: %d - %s" % (code,err))
    id = out
    
    username = "x509:%s" % fp
    user,created = User.objects.get_or_create(username=username)
    profile = user.get_profile()
    if created:
        profile.type = UserProfile.X509
        profile.home = name
        profile.display = "X509 Certificate (%s)" % (fp)
        profile.identifier = id
        
        add_member(profile.home,user)
        profile.save()
        
def home_name(user,short=None,autocreate=False):
    if short == None:
        short = user.username
    urn = lookup("urn",True)
    anyuser = lookup("system:anyuser",True)
    urn.setacl(anyuser,'rl')
    
    home = lookup('user:'+user.username,autocreate=autocreate)
    add_member(home,user,hidden=True)
    home.setpacl(home, "rwlida")
    home.setacl(home,"rwlia") #don't allow users to delete or reset acls on their home, nor invite members - that would be confusing as hell
    home.short = short
    home.save()
    
    return home

@login_required
def home(request):
    memberships = []
    try:
        memberships = Membership.objects.filter(user=request.user,hidden=False)
    except ObjectDoesNotExist:
        pass
    
    user = request.user
    profile = user.get_profile()
    if profile.home == None:
        cn = user.get_full_name()
        if not cn:
            cn = user.username
        profile.home = home_name(user, short=cn, autocreate=True)
    
    names = [(link.src,link.data) for link in NameLink.objects.filter(dst__memberships__user=request.user,type=NameLink.access_control,data__contains='i').all()]
    
    return respond_to(request, {'text/html': 'apps/userprofile/home.html'},{'memberships': memberships,'names': names})

@login_required
def add_sshkey(request,id=None):
    name = None
    if id == None:
        name = request.user.get_profile().home
    else:
        name = get_object_or_404(Name,pk=id)
    if name == None:
        return render403(request, "Homeless user.")
    if not name.has_permission(request.user,'i'):
        return render403(request,"You do not have permission to manage aliases here.")
    if not name.parent or name.parent.value != 'user':
        return render403(request,"This is the wrong place for that.")
    
    if request.method == 'POST':
        form = AddSSHKeyForm(request.POST)
        if form.is_valid():
            sshkey = form.cleaned_data['sshkey']
            keyfile = NamedTemporaryFile()
            keyfile.write(sshkey)
            keyfile.seek(0)
            _add_sshkey(name, keyfile)
            keyfile.close()
            return HttpResponseRedirect("/user/home")
    else:
        form = AddSSHKeyForm()
        
    return respond_to(request,{'text/html':'apps/userprofile/sshkey.html'},{'form':form})

@login_required
def add_cert(request,id=None):
    name = None
    if id == None:
        name = request.user.get_profile().home
    else:
        name = get_object_or_404(Name,pk=id)
    if name == None:
        return render403(request, "Homeless user.")
    if not name.has_permission(request.user,'i'):
        return render403(request,"You do not have permission to manage aliases here.")
    if not name.parent or name.parent.value != 'user':
        return render403(request,"This is the wrong place for that.")
    
    if request.method == 'POST':
        form = AddCertificateForm(request.POST)
        if form.is_valid():
            certificate = form.cleaned_data['certificate']
            keyfile = NamedTemporaryFile()
            keyfile.write(certificate)
            keyfile.seek(0)
            _add_gridcert(name, keyfile)
            keyfile.close()
            return HttpResponseRedirect("/user/home")
    else:
        form = AddCertificateForm()
        
    return respond_to(request,{'text/html':'apps/userprofile/cert.html'},{'form':form})

@login_required
def add_alias(request,id=None):
    name = None
    if id == None:
        name = request.user.get_profile().home
    else:
        name = get_object_or_404(Name,pk=id)
    if name == None:
        return render403(request, "Homeless user.")
    if not name.has_permission(request.user,'i'):
        return render403(request,"You do not have permission to manage aliases here.")
    if not name.parent or name.parent.value != 'user':
        return render403(request,"This is the wrong place for that.")
    
    return respond_to(request,{'text/html':'apps/userprofile/addalias.html'})

@login_required
def search(request):
    list = []
    if request.REQUEST.has_key('term'):
        term = request.REQUEST['term']
        list = [{'label': userdisplay(user),'value': user.id} 
                for user in User.objects.filter(Q(username__contains=term) | 
                                                Q(profile__display_name__contains=term) | 
                                                Q(profile__identifier__contains=term) | 
                                                Q(first_name__contains=term) |
                                                Q(last_name__contains=term))]
    return json_response(list)

@login_required
def info(request,username):
    user = get_object_or_404(User,username=username)
    return json_response({'username': user.username}); 