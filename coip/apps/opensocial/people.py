'''
Created on Jun 19, 2011

@author: leifj
'''
from django.contrib.auth.models import User
from coip.apps.opensocial.serializer import OpenSocialSerializer
from django.conf.urls.defaults import url
from coip.apps.membership.models import Membership
from tastypie.fields import ToOneField
from tastypie.utils.urls import trailing_slash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.http import HttpGone, HttpMultipleChoices
from coip.apps.name.models import Name
from tastypie.constants import ALL_WITH_RELATIONS
from django.shortcuts import get_object_or_404
import logging
from pprint import pformat
from coip.apps.opensocial.common import OpenSocialResource

class GroupResource(OpenSocialResource):
    
    class Meta:
        queryset = Name.objects.all()
        serializer = OpenSocialSerializer()
        resource_name = 'groups'
        fields = ['short','description','id']
        
        def override_urls(self):
            return [
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)/(?P<name_id>[\d]+)%s?" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('list_memberships'), name="api_list_memberships"),
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)%s" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('list_memberships'), name="api_list_memberships"), 
                url(r"^(?P<resource_name>%s)%s" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('list_memberships'), name="api_list_memberships"),
            ]
            
    def list_memberships(self, request, **kwargs):
        logging.debug(pformat(kwargs))
        try:
            user = self.cached_obj_get(request=request, username=kwargs['username'])
            logging.debug(pformat(user))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        group_resource = GroupResource()
        if kwargs.has_key('name_id'):
            name_id = kwargs.pop('name_id')
            return group_resource.get_list(request=request, pk=name_id)
        else:
            
            return 
        
    
    def dispatch(self, request_type, request, **kwargs):
        if kwargs.has_key('username') and kwargs['username'] == '@me':
            kwargs['username'] = request.user.username
        return super(GroupResource, self).dispatch(request_type, request, **kwargs)

class MembershipResource(OpenSocialResource):
    
    user = ToOneField("coip.apps.opensocial.people.PersonResource",'user',full=True)
    name = ToOneField("coip.apps.opensocial.people.GroupResource",'name',full=False)
    
    class Meta:
        queryset = Membership.objects.all()
        serializer = OpenSocialSerializer()
        resource_name = 'membership'
        fields = ['user','name']
        filtering = {
                     'name': ALL_WITH_RELATIONS
        } 

    def dehydrate(self,bundle):
        bundle = super(MembershipResource,self).dehydrate(bundle)
        del bundle.data['resource_uri']
        logging.debug(pformat(bundle))
        return bundle

class PersonResource(OpenSocialResource):
    
    #memberships = ToManyField(MembershipResource,'memberships',full=True)
    
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        resource_name = 'people'
        serializer = OpenSocialSerializer()
        
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)/(?P<name_id>[\d]+)%s?" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('list_memberships'), name="api_list_memberships"),
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)(?:/\@self)?%s" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
    
    def list_memberships(self, request, **kwargs):
        logging.debug(pformat(kwargs))
        try:
            user = self.cached_obj_get(request=request, username=kwargs['username'])
            logging.debug(pformat(user))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        people_resource = PersonResource()
        name_id = kwargs.pop('name_id')
        name = get_object_or_404(Name,id=name_id)
        return people_resource.get_list(request=request, memberships__name=name)
    
    def dispatch(self, request_type, request, **kwargs):
        if kwargs.has_key('username') and kwargs['username'] == '@me':
            kwargs['username'] = request.user.username
        return super(PersonResource, self).dispatch(request_type, request, **kwargs)
        
    def dehydrate(self,bundle):
        bundle = super(PersonResource,self).dehydrate(bundle)
        bundle.data['id'] = bundle.data['username']
        bundle.data['displayName'] = bundle.obj.get_profile().display_name
        del bundle.data['resource_uri']
        del bundle.data['username']
        return bundle