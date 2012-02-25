from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from campus_org.models import CampusOrg

class Command(BaseCommand):
    def handle(self, *args, **options):
        techfair_user = User.objects.get(email="techfair@mit.edu")
        techfair = CampusOrg.objects.get(name="Techfair")
        techfair.user = techfair_user;
        techfair.save();