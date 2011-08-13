import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from core.models import Language

for language in Language.objects.all():
    language.name_and_level = language.name
    language.name = language.name.split(" ")[0]
    language.save()