'''
Created on Jun 23, 2010

@author: leifj
'''
from django import forms
from coip.apps.membership.models import Membership

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
    
class InvitationForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['email']