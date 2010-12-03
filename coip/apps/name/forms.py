'''
Created on Jun 24, 2010

@author: leifj
'''
from django import forms
from coip.apps.name.models import Name, Attribute, NameLink
from django.forms import fields
from django.forms.widgets import HiddenInput, CheckboxSelectMultiple
    
class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute

class NameEditForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 6}))
    
    class Meta:
        model = Name
        fields = ['short','description']
        
class NewNameForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 6}))
    class Meta:
        model = Name
        fields = ['type','value','short','description']
        
class NameDeleteForm(forms.Form):
    recursive = fields.BooleanField(label="Also delete everything below this name?",required=False)
    
class NameLinkForm(forms.ModelForm):
    class Meta:
        model = NameLink
        fields = ['dst','type','data']

class NameLinkDeleteForm(forms.Form):
    confirm = fields.BooleanField(label="Confirm")
    
class PermissionForm(forms.Form):
    dst = fields.IntegerField(widget=HiddenInput)
    subject = fields.CharField(min_length=1024)
    permissions = fields.MultipleChoiceField(widget=CheckboxSelectMultiple,choices=[('r','read'),('w','write'),('l','list'),('i','insert'),('d','delete')])
