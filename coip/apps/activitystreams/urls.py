'''
Created on Nov 7, 2011

@author: leifj
'''
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('coip.apps.activitystreams.views',
    url(r'^@any/(?P<id>[0-9]+)/?$', view='name')
)