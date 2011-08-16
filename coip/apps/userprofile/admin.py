from django.contrib import admin
from coip.apps.userprofile.models import UserProfile, Identifier

admin.site.register(UserProfile)
admin.site.register(Identifier)