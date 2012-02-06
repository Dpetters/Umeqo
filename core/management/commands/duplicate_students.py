from core.utils import copy_model_instance

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from student.models import Student

class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(500, 2000):
            new_user = copy_model_instance(User.objects.all()[1])
            new_user.username = "%d_%s" % (i, new_user)
            new_user.email = "%d_%s" % (i, new_user)
            new_user.save()
            new_user.userattributes.is_verified = True
            new_user.userattributes.save()
            new_student = copy_model_instance(Student.objects.all()[0])
            new_student.user = new_user
            new_student.save()
            