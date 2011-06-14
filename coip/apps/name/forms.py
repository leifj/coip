'''
Created on Jun 24, 2010

@author: leifj
'''
from django import forms
from coip.apps.name.models import Name, Attribute, NameLink
from django.forms import fields
from django.forms.widgets import HiddenInput, CheckboxSelectMultiple, TextInput
from form_utils.forms import BetterModelForm, BetterForm
    
class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        
class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute

class NameEditForm(BetterModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Name
        fields = ['short','description','format']
        widgets = {'description': forms.Textarea(attrs={'cols': 62, 'rows': 6}),
                   'short':  forms.TextInput(attrs={'size': 40})}
        fieldsets = [('step1', {'fields': ['short', 'description'],
                                'legend': 'Name and Description',
                                'classes': ['step'], 
                                'description': 'Provide a short and (optionally) longer description of your group.'}),
                     ('step2', {'fields': ['format'],
                                'legend': 'Advanced',
                                'classes': ['step','submit_step'],
                                'description': 'Only change these settings if you know what you are doing.'})            
                    ]

class NewNameForm(BetterModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    value = forms.CharField(label="Name")
    #error_css_class = 'error'
    #required_css_class = 'required'
    class Meta:
        model = Name
        fields = ['value','short','description','type','format']
        widgets = {'description': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
                   'short':  forms.TextInput(attrs={'size': 40})}
        fieldsets = [('step1', {'fields': ['value'], 
                                'legend': 'Step 1: Name your group',
                                'classes': ['step'],
                                'description': 'Provide a short identifier for your groups. Spaces are not allowed here.'}),
                     ('step2', {'fields': ['short', 'description'],
                                'legend': 'Step 2: Describe your group',
                                'classes': ['step'], 
                                'description': 'Provide a short and (optionally) longer description of your group.'}),
                     ('step3', {'fields': ['type','format'],
                                'legend': 'Step 3 (optional): Advanced options',
                                'classes': ['step','submit_step'],
                                'description': 'Only change these settings if you know what you are doing...'})]
        
class NameDeleteForm(BetterForm):
    recursive = fields.BooleanField(label="Also delete everything below this name?",required=False)
    class Meta:
        fieldsets = [('step1', {'fields': ['recursive'], 
                                'legend': 'Confirm deletion of your group',
                                'classes': ['step'],
                                'description': 'This is a destructive operation - there is no way to recover your group once it has been deleted!'})]
    
class NameLinkForm(forms.ModelForm):
    class Meta:
        model = NameLink
        fields = ['dst','type','data']

class NameLinkDeleteForm(forms.Form):
    confirm = fields.BooleanField(label="Confirm")
    
class PermissionForm(BetterForm):
    dst = fields.IntegerField(widget=HiddenInput)
    subject = fields.CharField(max_length=1024,label="Group",widget=TextInput(attrs={'size': 40}))
    permissions = fields.MultipleChoiceField(widget=CheckboxSelectMultiple,
                                             choices=[('r','read'),
                                                      ('w','write'),
                                                      ('l','list members and groups'),
                                                      ('i','manage members'),
                                                      ('d','delete'),
                                                      ('a','manage access')])
    class Meta:
        fieldsets = [('subject',{'fields': ['dst','subject'],
                               'legend': 'Step 1: Select a group',
                               'classes': ['step'],
                               'description': 'Start typing in the textfield to find the group you want.'}),
                     ('permission',{'fields': ['permissions'],
                                    'legend': 'Step 2: Set permissions',
                                    'classes': ['step','submit_step'],
                                    'description': 'Select the rights that members of the group should have.'})]
        