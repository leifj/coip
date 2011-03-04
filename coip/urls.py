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
    (r'^user/(.+)/groups.json$',                    'coip.apps.name.views.user_groups'),
    (r'^user/search.json$',                         'coip.apps.userprofile.views.search'),
    (r'^user/info/(.+).json$',                      'coip.apps.userprofile.views.info'),
    # Invitations
    (r'^name/(?P<id>[0-9]+)/invite$',                'coip.apps.invitation.views.invite'),
    (r'^invitation/(?P<id>[0-9]+)/cancel$',          'coip.apps.invitation.views.cancel'),
    (r'^invitation/(?P<id>[0-9]+)/resend$',          'coip.apps.invitation.views.resend'),
    (r'^invitation/(?P<nonce>[^\/]+)/accept$',       'coip.apps.invitation.views.accept'),
    # Names
    (r'^name/id/(?P<id>[0-9]+)(?:\.([^\.]+))?$',     'coip.apps.name.views.show_by_id'),
    (r'^name$',                                      'coip.apps.name.views.show_root'),
    (r'^name/search.json$',                          'coip.apps.name.views.search'),
    (r'^name/(?P<id>[0-9]+)/edit$',                  'coip.apps.name.views.edit'),
    (r'^name/(?P<id>[0-9]+)/delete$',                'coip.apps.name.views.delete'),
    (r'^name/(?P<id>[0-9]+)/add$',                   'coip.apps.name.views.add'),
    (r'^name/(?P<id>[0-9]+)/join$',                  'coip.apps.membership.views.join'),
    (r'^name/(?P<id>[0-9]+)/join/(?P<membername>[^\/]+)$',                  'coip.apps.membership.views.join'),
    (r'^name/(?P<id>[0-9]+)/leave/(?P<membername>[^\/]+)$',                  'coip.apps.membership.views.leave'),
    # Name Links
    (r'^name/(?P<id>[0-9]+)/link/(?P<type>[0-9]+).json$',               'coip.apps.name.views.links'),
    # ACL
    (r'^name/(?P<id>[0-9]+)/acl/(?P<type>[0-9]+)$',         'coip.apps.name.views.lsacl'),
    (r'^name/(?P<id>[0-9]+)/acl/(?P<type>[0-9]+)/add$',     'coip.apps.name.views.addacl'),
    #(r'^name/(?P<id>[0-9]+)/acl/(?P<type>[0-9]+)/copy$',    'coip.apps.name.views.copyacl'),
    (r'^name/(?P<id>[0-9]+)/acl/(?P<aclid>[0-9]+)/remove$',  'coip.apps.name.views.rmacl'),
    # Links
    (r'^name/(?P<id>[0-9]+)/addlink$',               'coip.apps.link.views.add'),
    (r'^name/(?P<name>.+)(?:\.([^\.]+))?$',          'coip.apps.name.views.show_by_name'),
    (r'^link/(?P<id>[0-9]+)/remove$',                'coip.apps.link.views.remove'),
    # Membership
    (r'^membership/(?P<id>[0-9]+)$',                 'coip.apps.membership.views.show'),
    # Tags (eg roles on memberships and invitations)
    (r'^tag/(?P<type>(\S+))/(?P<id>[0-9]+)/modify$', 'coip.apps.tag.views.modify'),
    # JSON Tree
    (r'^ctree.json$',                                'coip.apps.name.views.ctree'),
    (r'^ctree/(?P<id>[0-9]+).json$',                 'coip.apps.name.views.ctree'),
    (r'^rtree.json$',                                'coip.apps.name.views.rtree'),
    (r'^rtree/(?P<id>[0-9]+).json$',                 'coip.apps.name.views.rtree'),
)
