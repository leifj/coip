'''
Created on Aug 19, 2011

@author: leifj
'''

from form_utils.forms import BetterForm
from django.forms.fields import CharField
from django.forms.widgets import Textarea


class AddSSHKeyForm(BetterForm):
    sshkey = CharField(label='SSH Key',widget=Textarea(attrs={'cols': 60, 'rows': 6}))
    class Meta:   
        fieldsets = [
                     ('key',{'fields':['sshkey'],
                             'legend': 'Please provide your SSH key.',
                             'description': 'Cut and paste your SSH key into the text field. Note that you should only submit the .pub-file and never the private key.',
                             'classes': ['step','submit_step']})
                     ]
        
class AddCertificateForm(BetterForm):
    certificate = CharField(label='PEM X509 Certificate',widget=Textarea(attrs={'cols': 60, 'rows': 6}))
    class Meta:   
        fieldsets = [
                     ('key',{'fields':['certificate'],
                             'legend': 'Please provide your personal certificate.',
                             'description': 'Cut and paste your PEM format X509 Certificate into the text field.',
                             'classes': ['step','submit_step']})
                     ]