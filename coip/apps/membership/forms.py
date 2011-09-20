'''
Created on Jun 23, 2010

@author: leifj
'''
from coip.apps.membership.models import Membership
from form_utils.forms import BetterModelForm
from django.forms.fields import CharField
from django.forms.widgets import HiddenInput, TextInput

class MembershipForm(BetterModelForm):
    username = CharField(label="User")
    class Meta:
        model = Membership
        fields = ['user']
        widgets = {
            'user': HiddenInput(),
            'username': TextInput(attrs={'size': 40})
        }
        fieldsets = [
                     ('user', {'fields': ['user','username'],
                                  'legend': 'Adding a user to the group',
                                  'description': 'Start typing to find the user to add. That user must have already logged in at least once. To add a user that has not yet logged in, send an invitation instead.',
                                  'classes': ['step','submit_step']})          
                    ]