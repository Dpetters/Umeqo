import string
import subprocess

from django.db.models.loading import get_models
loaded_models = get_models()
        
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from employer.models import Employer, Recruiter

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--update', action='store_true', dest='update', default=False, help='Mark each person (except those marked as final) as someone who will get emailed or not.'),
        )

    def handle(self, *args, **options):
        f = open("credentials.txt", "w")
        for employer in Employer.objects.all():
            if not employer.visible and not len(employer.recruiter_set.all()) > 0:
                username = employer.name.lower().replace(' ','').strip()[:10]
                exclude = set(string.punctuation)
                tmp = ''.join(ch for ch in username if ch not in exclude)
                username = "%s@%s.com" % (tmp[:5], tmp)
                p = subprocess.Popen("python passkool.py \"%s\" \"employer umeqo %s\" -l 6" % (username, employer.name), stdout=subprocess.PIPE, shell=True)
                p.wait()
                output = p.stdout.read()
                password = output.split(":")[1].strip()
                print >> f, "%s %s" % (username, password)
                user = User.objects.create(username=username, email=username, is_active = True)
                user.set_password(password)
                user.save()
                Recruiter.objects.create(user = user, employer=employer, is_master=True)
        f.close()                