'''
Created on Jun 19, 2011

@author: leifj
'''
from tastypie.resources import ModelResource
from coip.apps.userprofile.models import UserProfile, last_used_profile
from django.contrib.auth.models import User
from coip.apps.opensocial.serializer import OpenSocialSerializer
from django.conf.urls.defaults import url
from coip.apps.membership.models import Membership
from tastypie.fields import ToManyField, ToOneField
from tastypie.utils.urls import trailing_slash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.http import HttpGone, HttpMultipleChoices
import logging
from tastypie.serializers import Serializer
from pprint import pformat

class MembershipResource(ModelResource):
    
    user = ToOneField("coip.apps.opensocial.people.PersonResource",'user',full=True)
    
    class Meta:
        queryset = Membership.objects.all()
        serializer = OpenSocialSerializer()
        resource_name = 'membership'
        fields = ['user']

    def dehydrate(self,bundle):
        bundle = super(MembershipResource,self).dehydrate(bundle)
        del bundle.data['resource_uri']
        return bundle

class PersonResource(ModelResource):
    
    #memberships = ToManyField(MembershipResource,'memberships',full=True)
    
    class Meta:
        queryset = User.objects.all()
        fields = ['username']
        resource_name = 'people'
        serializer = OpenSocialSerializer()
        
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)/(?P<pk>[\d]+)%s?" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('list_memberships'), name="api_list_memberships"),
                url(r"^(?P<resource_name>%s)/(?P<username>[\@\w\d_.-:]+)(?:/\@self)?%s" % (self._meta.resource_name,trailing_slash()),
                    self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
    
    def list_memberships(self, request, **kwargs):
        logging.debug(pformat(kwargs))
        try:
            obj = self.cached_obj_get(request=request, username=kwargs['username'])
            logging.debug(pformat(obj))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        membership_resource = MembershipResource()
        return membership_resource.get_list(request, group__owner_id=obj.pk)
    
    def dispatch(self, request_type, request, **kwargs):
        if kwargs.has_key('username') and kwargs['username'] == '@me':
            kwargs['username'] = request.user.username
        return super(PersonResource, self).dispatch(request_type, request, **kwargs)
        
    def dehydrate(self,bundle):
        bundle = super(PersonResource,self).dehydrate(bundle)
        bundle.data['id'] = bundle.data['username']
        bundle.data['displayName'] = last_used_profile(bundle.obj).display_name
        del bundle.data['resource_uri']
        del bundle.data['username']
        return bundle