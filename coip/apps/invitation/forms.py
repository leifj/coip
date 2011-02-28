'''
Created on Jun 23, 2010

@author: leifj
'''
from django import forms
from coip.apps.invitation.models import Invitation
from form_utils.forms import BetterModelForm

class InvitationForm(BetterModelForm):
    class Meta:
        model = Invitation
        fields = ['email','message','expires']
        fieldsets = [('step1', {'fields': ['email','message'], 
                                'legend': 'Step 1: Email and message',
                                'classes': ['step'],
                                'description': 'An email message will be sent to the recipient with an invitation-link. After following that link the recipient will be a member of the group.'}),
                    ('step2', {'fields': ['expires'],
                               'legend': 'Step 2: Expiration (optioinal)',
                               'classes': ['step','submit_step'],
                               'description': 'You are encouraged to provide an expiration time for your invitation. The time should be long enough to allow the recipient to answer and short enough prevent the invitation from falling into the wrong hands. The default is usually good enough.'})
                                ]