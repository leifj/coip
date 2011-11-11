'''
Created on Nov 7, 2011

@author: leifj
'''
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('coip.apps.opensocial.views',
    url(r'^rpc$',view='rpc'),
    url(r'^people/(?P<uid>.+)$', view='person'),
    url(r'^people/(?P<uid>.+)/(?P<gid>.+)$', view='person'),
    url(r'^groups/(?P<uid>.+)$', view='group'),
    url(r'^activitystreams/', include('coip.apps.activitystreams.urls'))
)