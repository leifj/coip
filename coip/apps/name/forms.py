'''
Created on Jun 24, 2010

@author: leifj
'''
from django import forms
from coip.apps.name.models import Name, Attribute
    
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