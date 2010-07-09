from django.contrib import admin
from coip.apps.name.models import Name, Attribute, NameLink

admin.site.register(Name)
admin.site.register(Attribute)
admin.site.register(NameLink)