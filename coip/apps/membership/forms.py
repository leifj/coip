'''
Created on Jun 23, 2010

@author: leifj
'''
from django import forms
from coip.apps.membership.models import Membership
from django.forms.widgets import Textarea

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
    
class InvitationForm(forms.Form):
    email = forms.EmailField()
    expires = forms.DateTimeField()
    message = forms.CharField(widget=Textarea)