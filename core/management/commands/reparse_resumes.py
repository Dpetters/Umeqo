from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import Q

from student.enums import RESUME_PROBLEMS
from student.models import Student
from student.view_helpers import process_resume

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--win', action='store_true', dest='win', default=False, help='Use the version of pdftotext for windows.'),
        make_option('--all', action='store_true', dest='all', default=False, help='Reparse all resumes.'),
        make_option('--dry', action='store_true', dest='dry', default=False, help='Print out the names of people whose resumes could not be parsed for keywords.'),
    )
    
    def handle(self, *args, **options):
        try:
            hacked_resumes = []
            unparsable_resumes = []
            
            students = Student.objects.filter(profile_created=True, user__is_active=True)
            if not options["all"]:
                students = students.filter(Q(keywords=None) | Q(keywords=""))
            for student in students:
                name = "%s %s" % (student.first_name, student.last_name)
                if options['dry']:
                    print name
                else:
                    results = process_resume(student)
                    if results == RESUME_PROBLEMS.HACKED:
                        hacked_resumes.append(name)
                    elif results == RESUME_PROBLEMS.UNPARSABLE:
                        unparsable_resumes.append(name)
            if hacked_resumes:
                print "Hacked resumes: %s" % (", ".join(hacked_resumes))
            if unparsable_resumes:
                print "Unparsable resumes: %s" % (", ".join(unparsable_resumes))
        except Exception as e:
            print e