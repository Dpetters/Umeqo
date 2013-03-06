import os
import re
import shutil
import csv

from time import strftime, gmtime

from django.conf import settings as s
from django.core.management.base import BaseCommand

from student.models import Student


def student_dump_csv():
    now = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    print "dumping users %s on %s" % (s.SITE_NAME, now)
    try:
    	csv_dump_dir = "%s" % s.CSV_DUMP_DIRECTORY
    	if not os.path.exists(csv_dump_dir):
            os.makedirs(csv_dump_dir)
    	f = open(csv_dump_dir + "student_dump.csv", "w")
    	writer = csv.writer(f)
    	writer.writerow( ('First Name', 'Last Name', 'Email') )
    	for student in Student.objects.filter(profile_created=True, user__is_active=True):
    		writer.writerow( (student.first_name, student.last_name, student.user.email) )

    except Exception as e:
        print "failed to dump students on: %s " % str(e)
    else:
        print "successfully dumped students to csv"


class Command(BaseCommand):    
    def handle(self, *args, **options):
        student_dump_csv()