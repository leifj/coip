'''
Created on Aug 4, 2010

@author: leifj
'''
from django import forms
from coip.apps.link.models import Link

class AddRelatedLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url','text']