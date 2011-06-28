import os
import sys

sys.path.append('/var/www/umeqo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import site
site.addsitedir('/usr/local/pythonenv/UMEQO/lib/python2.6/site-packages')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
