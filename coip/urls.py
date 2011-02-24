from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login
from settings import ADMIN_MEDIA_ROOT
from settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from coip.apps.auth.views import logout
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
    (r'^accounts/logout$',                          logout),
    (r'^accounts/login-federated/$',                'coip.apps.auth.views.accounts_login_federated'),
    (r'^accounts/logout/$',                         'coip.apps.auth.views.logout'),
    # Profiles and user information
    (r'^user/merge/(?P<pkey>.+)$',                  'coip.apps.userprofile.views.merge'),
    (r'^user/merge$',                               'coip.apps.userprofile.views.merge'),
    (r'^user/home$',                                'coip.apps.userprofile.views.home'),
    # Invitations
    (r'^name/(?P<id>[0-9]+)/invite$',                'coip.apps.invitation.views.invite'),
    (r'^invitation/(?P<id>[0-9]+)/cancel$',          'coip.apps.invitation.views.cancel'),
    (r'^invitation/(?P<id>[0-9]+)/resend$',          'coip.apps.invitation.views.resend'),
    (r'^invitation/(?P<nonce>[^\/]+)/accept$',       'coip.apps.invitation.views.accept'),
    # Names
    (r'^name/id/(?P<id>[0-9]+)$',                    'coip.apps.name.views.show_by_id'),
    (r'^name$',                                      'coip.apps.name.views.show_root'),
    (r'^name/(?P<id>[0-9]+)/edit$',                  'coip.apps.name.views.edit'),
    (r'^name/(?P<id>[0-9]+)/delete$',                'coip.apps.name.views.delete'),
    (r'^name/(?P<id>[0-9]+)/add$',                   'coip.apps.name.views.add'),
    (r'^name/(?P<name>.+)$',                         'coip.apps.name.views.show_by_name'),
    # Name Links
    (r'^name/(?P<id>[0-9]+)/link/(?P<type>[0-9]+).json$',               'coip.apps.name.views.links'),
    (r'^namelink/(?P<id>[0-9]+)/remove$',               'coip.apps.name.views.removelink'),
    (r'^name/(?P<id>[0-9]+)/link/(?P<type>[0-9]+)$',    'coip.apps.name.views.editacl'),
    # Links
    (r'^name/(?P<id>[0-9]+)/addlink$',               'coip.apps.link.views.add'),
    (r'^link/(?P<id>[0-9]+)/remove$',                'coip.apps.link.views.remove'),
    # Membership
    (r'^membership/(?P<id>[0-9]+)$',                 'coip.apps.membership.views.show'),
    # JSON Tree
    (r'^ctree.json$',                                'coip.apps.name.views.ctree'),
    (r'^ctree/(?P<id>[0-9]+).json$',                 'coip.apps.name.views.ctree'),
    (r'^rtree.json$',                                'coip.apps.name.views.rtree'),
    (r'^rtree/(?P<id>[0-9]+).json$',                 'coip.apps.name.views.rtree'),
)
