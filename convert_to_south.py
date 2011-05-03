import subprocess, os
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

for app in settings.INSTALLED_APPS:
    if app[:14] != "django.contrib":
        p = subprocess.Popen("python manage.py convert_to_south " + app, shell=True)
        p.wait()
