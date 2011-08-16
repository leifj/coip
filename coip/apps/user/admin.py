from django.contrib import admin
from coip.apps.user.models import Identifier, UserProfile

admin.site.register(Identifier)
admin.site.register(UserProfile)
