'''
Created on Aug 18, 2011

@author: leifj
'''
from coip.settings import METADATA
from lxml import etree
from hashlib import sha1
from django.contrib.auth.models import User
from coip.apps.name.models import lookup
from coip.apps.userprofile.models import UserProfile
from coip.apps.membership.models import add_member
from celery.decorators import periodic_task
from celery.schedules import crontab

@periodic_task(run_every=crontab(hour="*", minute="*/3", day_of_week="*"))
def import_metadata():
    doc = etree.parse(METADATA)
    ns = {'md': 'urn:oasis:names:tc:SAML:2.0:metadata',
          'xml': 'http://www.w3.org/XML/1998/namespace'}
    for e in doc.xpath("md:EntityDescriptor",namespaces=ns):
        entityId = e.get('entityID')
        print entityId
        display = entityId
        x = e.xpath("md:OrganizationDisplayName",namespaces=ns)
        if x:
            display = x[0]    
        
        username = "entity:%s" % sha1(entityId).hexdigest()
        (user,created) = User.objects.get_or_create(username=username)
        save = created
        profile = user.get_profile()

        if created:
            anyuser = lookup("system:anyuser")
            anyentity = lookup("system:anyentity",True)
            anyentity.setacl(anyuser, "rl")
            profile.type = UserProfile.ENTITY
            profile.home = anyentity
            add_member(anyentity, user)
        
        if display != profile.display_name:
            profile.display_name = display
            save = True
            
        if save:
            user.save()
            profile.save()