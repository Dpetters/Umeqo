import os
import sys
import site

site.addsitedir('/usr/local/pythonenv/UMEQO_DEMO/lib/python2.6/site-packages')

os.environ['PYTHON_EGG_CACHE'] = '/var/www/umeqo/apache/egg-cache'

sys.path.append('/var/www')
os.environ['DJANGO_SETTINGS_MODULE'] =

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
