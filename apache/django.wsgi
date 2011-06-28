import os
import sys
import site

site.addsitedir('/usr/local/pythonenv/UMEQO/lib/python2.6/site-packages')

os.environ['PYTHON_EGG_CACHE'] = '/var/www/umeqo/apache/egg-cache'

sys.path.append('/var/www/umeqo')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
