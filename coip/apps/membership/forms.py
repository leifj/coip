'''
Created on Jun 23, 2010

@author: leifj
'''
from coip.apps.membership.models import Membership
from form_utils.forms import BetterModelForm
from django.forms.fields import ChoiceField, CharField
from django.forms.widgets import Select, HiddenInput

class MembershipForm(BetterModelForm):
    type = ChoiceField(choices=(("user","I'm adding a user to the group"),("entity","I'm adding a relying party (SP or IdP) to the group")), label="", widget=Select(attrs={'class':'link'}), required=False, initial="user")
    username = CharField(label="Username")
    class Meta:
        model = Membership
        fields = ['entity','user']
        widgets = {
            'user': HiddenInput()
        }
        fieldsets = [('type', {'fields': ['type'], 
                               'legend': 'Which type of member are you adding to the group?',
                               'description': 'Groups can consist of users and/or relying partys. Adding a relying party to a group limits can be useful if you want to limit the visibility of your group. This is an advanced option and you should know what you are doing.',
                               'classes': ['step']}),
                     ('entity', {'fields': ['entity'],
                                  'legend': 'Adding a federation entity to the group',
                                  'description': 'Select the relying party you wish to add to the group.',
                                  'classes': ['step','submit_step']}),
                     ('user', {'fields': ['user','username'],
                                  'legend': 'Adding a user to the group',
                                  'description': 'Provide the federation identifier of the user you wish to join. That user must have already logged in at least once. To add a user that has not yet logged in, send an invitation instead.',
                                  'classes': ['step','submit_step']})          
                    ]