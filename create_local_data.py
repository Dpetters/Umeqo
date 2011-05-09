"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

""" 
This script is meant to populate the database with some fake non-fixturable data.
"""

import os, datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
ROOT = os.path.dirname(os.path.realpath("__file__"))

from django.conf import settings
from django.contrib.auth.models import User

from events.models import Event, EventType
from core.models import Industry
from employer.models import Employer

PASSWORD_TO_FAKE_ACCOUNTS = "Jamb4Juic3"

SAMPLE_EMPLOYER_USERNAME_1 = "SampleEmployer1"
SAMPLE_EMPLOYER_COMPANY_NAME_1 = "Sample Employer 1"
SAMPLE_EMPLOYER_EMAIL_1 = "sample@employer1.com"

SAMPLE_EMPLOYER_USERNAME_2 = "SampleEmployer2"
SAMPLE_EMPLOYER_COMPANY_NAME_2 = "Sample Employer 2"
SAMPLE_EMPLOYER_EMAIL_2 = "sample@employer2.com"

SAMPLE_EMPLOYER_USERNAME_3 = "SampleEmployer3"
SAMPLE_EMPLOYER_COMPANY_NAME_3 = "Sample Employer 3"
SAMPLE_EMPLOYER_EMAIL_3 = "sample@employer3.com"


# Helper Function
def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# Delete old search index files
delete_contents(settings.HAYSTACK_XAPIAN_PATH)    


# Delete the old submitted resumes
submitted_resumes_path = ROOT + "/media/submitted_resumes/"
delete_contents(submitted_resumes_path)

# Delete the old submitted user images
submitted_user_images_path = ROOT + "/media/submitted_user_images/"
delete_contents(submitted_user_images_path)

#Create sample employer users
sample_employer_user1 = User.objects.create(username = SAMPLE_EMPLOYER_USERNAME_1,
                                            email = SAMPLE_EMPLOYER_EMAIL_1)
sample_employer_user1.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
sample_employer_user1.save()

sample_employer_user2 = User.objects.create(username = SAMPLE_EMPLOYER_USERNAME_2,
                                            email = SAMPLE_EMPLOYER_EMAIL_2)
sample_employer_user2.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
sample_employer_user2.save()

sample_employer_user3 = User.objects.create(username = SAMPLE_EMPLOYER_USERNAME_3,
                                            email = SAMPLE_EMPLOYER_EMAIL_3)
sample_employer_user3.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
sample_employer_user3.save()
print "Created Employer User Accounts"


# Create Employers
sample_employer1 = Employer.objects.create(user=sample_employer_user1,
                                          company_name=SAMPLE_EMPLOYER_COMPANY_NAME_1,
                                          contact_phone="9999999999")
sample_employer1.industries.add(Industry.objects.get(name__exact="Financial"))

sample_employer2 = Employer.objects.create(user=sample_employer_user2,
                                          company_name=SAMPLE_EMPLOYER_COMPANY_NAME_2,
                                          contact_phone="9999999999")
sample_employer2.industries.add(Industry.objects.get(name__exact="Entrepreneurial/Start-Ups"))
sample_employer2.industries.add(Industry.objects.get(name__exact="Internet"))

sample_employer3 = Employer.objects.create(user=sample_employer_user3,
                                          company_name=SAMPLE_EMPLOYER_COMPANY_NAME_3,
                                          contact_phone="9999999999")
print "Created Employers"

# Create Events
Event.objects.create(employer=sample_employer1,
                     name="Weiss Asset Management Info Session",
                     start_datetime=datetime.datetime(2011, 11, 10, 17, 53, 59),
                     end_datetime=datetime.datetime(2011, 11, 10, 18, 53, 59),
                     type = EventType.objects.get(name="Info Session"),
                     location="3-217",
                     description="Learn more about the organization and meet company representatives in a less formal situation than an interview. You have the opportunity to ask questions (not about salary, please) in advance of the interview.")

Event.objects.create(employer=sample_employer1,
                     name="Google Internship Resume Drop Deadline",
                     end_datetime=datetime.datetime(2011, 6, 10, 18, 23, 59),
                     type = EventType.objects.get(name="Deadline"),
                     description="Get your resume to us if you want to be considered for an interview!")

Event.objects.create(employer=sample_employer1,
                     name="Morgan Stanley MIT Alumni Panel",
                     start_datetime=datetime.datetime(2011, 7, 10, 17, 53, 59),
                     end_datetime=datetime.datetime(2011, 7, 10, 19, 53, 59),
                     type = EventType.objects.get(name="Panel"),
                     location="10-250",
                     description="See what MIT Alumni have to say about working for our company.")

Event.objects.create(employer=sample_employer2,
                     name="Goldman Sachs Networking Event",
                     start_datetime=datetime.datetime(2011, 4, 10, 17, 53, 59),
                     end_datetime=datetime.datetime(2011, 4, 10, 18, 53, 59),
                     type = EventType.objects.get(name="Networking"),
                     location="Marriot",
                     description="Learn more about the organization and meet company representatives in a less formal situation than an interview.")

Event.objects.create(employer=sample_employer2,
                     name="Thomson Reuters Interview Sign-up Deadline",
                     start_datetime=datetime.datetime(2011, 5, 23, 17, 53, 59),
                     end_datetime=datetime.datetime(2011, 4, 10, 18, 53, 59),
                     type = EventType.objects.get(name="Deadline"),
                     description="Make sure to sign up for an interview by going to cnn.com")
print "Created Events"