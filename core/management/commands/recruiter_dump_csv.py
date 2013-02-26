import os
import re
import shutil
import csv

from time import strftime, gmtime

from django.conf import settings as s
from django.core.management.base import BaseCommand

from employer.models import Recruiter


def recruiter_dump_csv():
    now = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    print "dumping users %s on %s" % (s.SITE_NAME, now)
    try:
    	csv_dump_dir = "%s" % s.CSV_DUMP_DIRECTORY
    	if not os.path.exists(csv_dump_dir):
            os.makedirs(csv_dump_dir)
    	f = open(csv_dump_dir + "recruiter_dump.csv", "w")
    	writer = csv.writer(f)
    	writer.writerow( ('First Name', 'Last Name', 'Email') )
    	for recruiter in Recruiter.objects.filter():
    		writer.writerow( (recruiter.user.first_name, recruiter.user.last_name, recruiter.user.email) )

    except Exception as e:
        print "failed to dump recruiters on: %s " % str(e)
    else:
        print "successfully dumped recruiters to csv"


class Command(BaseCommand):    
    def handle(self, *args, **options):
        recruiter_dump_csv()