'''
Created on Jun 18, 2011

@author: leifj
'''
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from coip.apps.name.models import Name

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()

class NameResource(ModelResource):
    class Meta:
        queryset = Name.objects.all()