import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'coip.settings'

sys.path.append('/var/www/coip')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
