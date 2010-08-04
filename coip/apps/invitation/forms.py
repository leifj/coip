'''
Created on Jun 23, 2010

@author: leifj
'''
from django import forms
from coip.apps.invitation.models import Invitation

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email','message','expires']