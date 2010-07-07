from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login
from settings import ADMIN_MEDIA_ROOT
from settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
admin.autodiscover()

def welcome(request):
    return HttpResponseRedirect('/user/home')

urlpatterns = patterns('',
    (r'^admin-media/(?P<path>.*)$',                 'django.views.static.serve',{'document_root': ADMIN_MEDIA_ROOT}),
    (r'^site-media/(?P<path>.*)$',                  'django.views.static.serve',{'document_root': MEDIA_ROOT}),
    (r'^admin/',                                    include(admin.site.urls)),
    (r'^$',                                         welcome),
    # Login/Logout
    (r'^accounts/login/$',                          login,{'template_name': "login.html"}),
    (r'^accounts/login-federated/$',                'coip.apps.auth.views.accounts_login_federated'),
    (r'^accounts/logout/$',                         'coip.apps.auth.views.logout'),
    # Profiles and user information
    (r'^user/merge/(?P<pkey>.+)$',                  'coip.apps.userprofile.views.merge'),
    (r'^user/merge$',                               'coip.apps.userprofile.views.merge'),
    (r'^user/home$',                                'coip.apps.userprofile.views.home'),
    # Names
    (r'^name/id/(?P<id>[0-9]+)$',                    'coip.apps.name.views.show_by_id'),
    (r'^name/(?P<name>[^\/]+)$',                     'coip.apps.name.views.show_by_name'),
)
