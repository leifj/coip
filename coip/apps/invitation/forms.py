'''
Created on Jul 5, 2010

@author: leifj
'''
from django import forms
from coip.apps.invitation.models import Invitation

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation