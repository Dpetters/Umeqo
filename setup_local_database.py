"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

""" 
This script is meant to populate the database with the initial content for the site.

Note that in order for this file to work, the initial_contents folder has remain in
the the same directory as this script.
"""

# Don't switch the order the next three sections!

# Must remain first
import subprocess, os, datetime

# Must remain second
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
ROOT = os.path.dirname(os.path.realpath("__file__"))

# Must remain third
from django.conf import settings
from django.utils import simplejson
from django.contrib.auth.models import User

from help.models import Topic, Question
from help import enums as help_enums
from employer import enums as employer_enums
from events.models import Event, EventType, RSVPType
from core.models import Industry, GraduationYear, SchoolYear, Language, Course, CampusOrg, CampusOrgType, EmploymentType
from employer.models import Employer
from student.models import Student, StudentList
from student import enums as student_enums
from student import constants as student_constants

# Change the following email to yours. All emails sent 
#to the fake accounts will then go there.
YOUR_EMAIL = "dpetters@mit.edu"

PASSWORD_TO_FAKE_ACCOUNTS = "Jamb4Juic3"

ADMIN_USERNAME = "admin"

SAMPLE_EMPLOYER_USERNAME_1 = "SampleEmployer1"
SAMPLE_EMPLOYER_COMPANY_NAME_1 = "Sample Employer 1"
SAMPLE_EMPLOYER_EMAIL_1 = "sample@employer1.com"

SAMPLE_EMPLOYER_USERNAME_2 = "SampleEmployer2"
SAMPLE_EMPLOYER_COMPANY_NAME_2 = "Sample Employer 2"
SAMPLE_EMPLOYER_EMAIL_2 = "sample@employer2.com"

# Helper Function
def delete_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
                          
# Delete old database file if it exists
if os.path.exists(settings.DATABASES['default']['NAME']):
    os.remove(settings.DATABASES['default']['NAME'])



# Delete old search index files
delete_contents(settings.HAYSTACK_XAPIAN_PATH)    



# Delete the old submitted resumes
submitted_resumes_path = ROOT + "/media/submitted_resumes/"
delete_contents(submitted_resumes_path)



# Important - if we're local, have the following be just python manage.py...
# If on the server though, change it to be python2.6 manage.py....
p = subprocess.Popen("python manage.py syncdb --noinput", shell=True)
p.wait()
p = subprocess.Popen("python manage.py createsuperuser --username " + ADMIN_USERNAME + " --email " + YOUR_EMAIL + " --noinput", shell = True)
p.wait()



#Give password to superuser
#Add superuser to the student group
admin_user = User.objects.get(username__exact=ADMIN_USERNAME)
admin_user.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
admin_user.save()
print "Created Super User"

# Create Student
sample_student = Student.objects.create(user = admin_user)


#Create sample employer users
sample_employer_user1 = User.objects.create(username = SAMPLE_EMPLOYER_USERNAME_1,
                                      email = SAMPLE_EMPLOYER_EMAIL_1)
sample_employer_user1.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
sample_employer_user1.save()

sample_employer_user2 = User.objects.create(username = SAMPLE_EMPLOYER_USERNAME_2,
                                      email = SAMPLE_EMPLOYER_EMAIL_2)
sample_employer_user2.set_password(PASSWORD_TO_FAKE_ACCOUNTS)
sample_employer_user2.save()
print "Created Employer User Accounts"

# Create FAQ Topics
basics_topic = Topic.objects.create(name="Basics", slug="basics", sort_order=0, audience=help_enums.ALL)

employer_registration = Topic.objects.create(name="Registration", slug="registration", sort_order=0, audience=help_enums.EMPLOYER)
employer_account_management = Topic.objects.create(name="Account Management", slug="account-management", sort_order=1, audience=help_enums.EMPLOYER)
employer_student_filtering = Topic.objects.create(name="Student Filtering", slug="student-filtering", sort_order=2, audience=help_enums.EMPLOYER)
employer_resumebooks = Topic.objects.create(name="Resumebooks", slug="resumebooks", sort_order=3, audience=help_enums.EMPLOYER)
employer_events = Topic.objects.create(name="Events", slug="events", sort_order=4, audience=help_enums.EMPLOYER)
employer_invitations = Topic.objects.create(name="Invitations", slug="invitations", sort_order=5, audience=help_enums.EMPLOYER)

student_registration = Topic.objects.create(name="Registration", slug="registration", sort_order=0, audience=help_enums.STUDENT)
student_account_management = Topic.objects.create(name="Account Management", slug="account-management", sort_order=1, audience=help_enums.STUDENT)
student_employer_subscriptions = Topic.objects.create(name="Employer Subscriptions", slug="employer_subscriptions", sort_order=2, audience=help_enums.STUDENT)
student_events = Topic.objects.create(name="Events", slug="events", sort_order=3, audience=help_enums.STUDENT)
student_invitations = Topic.objects.create(name="Invitations", slug="invitations", sort_order=4, audience=help_enums.STUDENT)

# Create FAQ Questions
Question.objects.create(topic=basics_topic, question="What is Umeqo?", slug="what-is-umeqo", answer="Umeqo is a new platform for helping students and employers connect during recruiting season.", status=help_enums.ACTIVE, audience=help_enums.ALL, sort_order=0)

# Create Industries
new_contents_path = ROOT + "/initial_content/Industries/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    Industry.objects.create(name=name)
print "Created Industries"



# Create Employers
sample_employer1 = Employer.objects.create(user=sample_employer_user1,
                                          company_name=SAMPLE_EMPLOYER_COMPANY_NAME_1,
                                          contact_phone="9999999999")
sample_employer1.industries.add(Industry.objects.get(name__exact="Financial Data Services"))

sample_employer2 = Employer.objects.create(user=sample_employer_user2,
                                          company_name=SAMPLE_EMPLOYER_COMPANY_NAME_2,
                                          contact_phone="9999999999")
sample_employer2.industries.add(Industry.objects.get(name__exact="Trucking & Truck Leasing"))
sample_employer2.industries.add(Industry.objects.get(name__exact="Waste Management"))
print "Created Employers"

# Create Student Lists 
all_students = StudentList.objects.create(name=student_constants.ALL_STUDENT_GROUP_NAME, sort_order=1, type=student_enums.GENERAL)
all_students.students.add(*list(Student.objects.filter(active=True)))
all_students.employers.add(*list(Employer.objects.filter(subscriber=True)))
print "Created Student Lists"

# Create Graduation Years
new_contents_path = ROOT + "/initial_content/GraduationYears/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for year in contents:
    print year
    GraduationYear.objects.create(year=year)
print "Created Graduation Years"

# Create Employment Types
new_contents_path = ROOT + "/initial_content/EmploymentTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for type in contents:
    print type
    EmploymentType.objects.create(name=type)
print "Created Employment Types"

# Create School Years
new_contents_path = ROOT + "/initial_content/SchoolYears/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    SchoolYear.objects.create(name=name)
print "Created School Years"



# Create Languages
new_contents_path = ROOT + "/initial_content/Languages/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    Language.objects.create(name=name)
print "Created Languages"



# Create Courses
existing_contents_path =  ROOT + "/media/submitted_images/Courses/"
delete_contents(existing_contents_path)

new_contents_path = ROOT + "/initial_content/Courses/"

for f in os.listdir(new_contents_path):
    if os.path.isdir(os.path.join(new_contents_path, f)):
        contents_file = open(new_contents_path + f + "/contents.json")
        contents = simplejson.loads(contents_file.read())
        
        if not contents.has_key("name"):
            raise Exception(f + ": name not provided")
        if not contents.has_key("num"):
            raise Exception(f + ": course number not provided")

        name = contents["name"]
        print name
        
        num = contents["num"]

        admin = ""
        if contents.has_key("admin"):
            admin = contents["admin"]
                    
        email = ""
        if contents.has_key("email"):
            email = contents["email"]
        
        website = ""
        if contents.has_key("website"):
            website = contents["website"]

        description = ""
        if contents.has_key("description"):
            description = contents["description"]

        if contents.has_key("sort_order"):
            sort_order = contents["sort_order"]
            
        Course.objects.create(name = name, num = num, email = email, website = website, description = description, sort_order=sort_order)
print "Created Courses"



# Create Campus Organization Types
new_contents_path = ROOT + "/initial_content/CampusOrgTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    CampusOrgType.objects.create(name=name)
print "Created Campus Organization Types"



# Create Campus Organizations
existing_contents_path =  ROOT + "/media/submitted_images/CampusOrgs/"
delete_contents(existing_contents_path)

new_contents_path = ROOT + "/initial_content/CampusOrgs/"

for f in os.listdir(new_contents_path):
    if os.path.isdir(os.path.join(new_contents_path, f)):
        contents_file = open(new_contents_path + f + "/contents.json")
        contents = simplejson.loads(contents_file.read())
        
        if not contents.has_key("name"):
            raise Exception(f + ": name not provided")
        if not contents.has_key("type"):
            raise Exception(f + ": CampusOrgType not provided")

        name = contents["name"]
        print name
        
        type_name = contents["type"]
        type = CampusOrgType.objects.get(name=type_name)
        
        email = ""
        if contents.has_key("email"):
            email = contents["email"]
        
        website = ""
        if contents.has_key("website"):
            website = contents["website"]

        description = ""
        if contents.has_key("description"):
            description = contents["description"]

        CampusOrg.objects.create(name = name, type = type, email = email, website = website, description = description)

print "Created Campus Organizations"



#Create RSVP Types
new_contents_path = ROOT + "/initial_content/RSVPTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    RSVPType.objects.create(name=name)
print "Created RSVP Types"



#Create EventTypes
new_contents_path = ROOT + "/initial_content/EventTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    EventType.objects.create(name=name)
print "Created Event Types"



#Create Events
existing_contents_path =  ROOT + "/media/submitted_images/Events/"
delete_contents(existing_contents_path)

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