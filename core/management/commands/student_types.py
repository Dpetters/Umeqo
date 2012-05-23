from django.core.management.base import BaseCommand

from student.models import Student, StudentType

class Command(BaseCommand):
    def handle(self, *args, **options):
        grad_phd = StudentType.objects.get(name="Graduate - PHD")
        grad_masters = StudentType.objects.get(name="Graduate - Masters")
        undergrad = StudentType.objects.get(name="Undergraduate")
        
        for student in Student.objects.filter(profile_created=True):
            if student.school_year.name == "Graduate - PHD":
                student.type = grad_phd
            elif student.school_year.name == "Graduate - Masters":
                student.type = grad_masters
            else:
                student.type = undergrad
            student.save() 