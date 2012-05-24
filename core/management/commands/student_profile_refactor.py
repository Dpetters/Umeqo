from django.core.management.base import BaseCommand

from student.models import Student, DegreeProgram

class Command(BaseCommand):
    def handle(self, *args, **options):
        grad_phd = DegreeProgram.objects.get(name="Research Doctorate Degree")
        grad_masters = DegreeProgram.objects.get(name="Master's Degree")
        undergrad = DegreeProgram.objects.get(name="Bachelors Degree")
        
        for student in Student.objects.filter(profile_created=True):
            if student.school_year.name == "Graduate - PHD":
                student.degree_program = grad_phd
            elif student.school_year.name == "Graduate - Masters":
                student.degree_program = grad_masters
            else:
                student.degree_program = undergrad
            student.save() 