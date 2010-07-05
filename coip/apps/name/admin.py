from django.contrib import admin
from coip.apps.name.models import Name, Attribute

admin.site.register(Name)
admin.site.register(Attribute)