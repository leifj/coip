'''
Created on Jun 24, 2010

@author: leifj
'''
from django import forms
from coip.apps.name.models import Name, Attribute, NameLink
from django.forms.fields import BooleanField
    
class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute

class NameEditForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ['short','description']
        
class NewNameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ['type','value','short','description']
        
class NameDeleteForm(forms.Form):
    recursive = BooleanField(label="Also delete all nodes below this node?",required=False)
    confirm = BooleanField(label="Confirm")
    
class NameLinkForm(forms.ModelForm):
    class Meta:
        model = NameLink
        fields = ['dst','type','data']

class NameLinkDeleteForm(forms.Form):
    confirm = BooleanField(label="Confirm")