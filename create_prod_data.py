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
import os

# Must remain second
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
ROOT = os.path.dirname(os.path.realpath("__file__"))

from django.utils import simplejson

from core import enums
from core.models import Industry, EventType, GraduationYear, SchoolYear, Language, Course, CampusOrg, CampusOrgType, EmploymentType, Topic, Question
from employer.models import Employer
from student.models import Student, StudentList
from student import enums as student_enums
from student import constants as student_constants

# Create FAQ Topics
basics_topic = Topic.objects.create(name="Basics", slug="basics", sort_order=0, audience=enums.ALL)

employer_registration = Topic.objects.create(name="Registration", slug="registration", sort_order=0, audience=enums.EMPLOYER)
employer_account_management = Topic.objects.create(name="Account Management", slug="account-management", sort_order=1, audience=enums.EMPLOYER)
employer_student_filtering = Topic.objects.create(name="Student Filtering", slug="student-filtering", sort_order=2, audience=enums.EMPLOYER)
employer_resumebooks = Topic.objects.create(name="Resumebooks", slug="resumebooks", sort_order=3, audience=enums.EMPLOYER)
employer_events = Topic.objects.create(name="Events", slug="events", sort_order=4, audience=enums.EMPLOYER)
employer_invitations = Topic.objects.create(name="Invitations", slug="invitations", sort_order=5, audience=enums.EMPLOYER)

student_registration = Topic.objects.create(name="Registration", slug="registration", sort_order=0, audience=enums.STUDENT)
student_account_management = Topic.objects.create(name="Account Management", slug="account-management", sort_order=1, audience=enums.STUDENT)
student_employer_subscriptions = Topic.objects.create(name="Employer Subscriptions", slug="employer_subscriptions", sort_order=2, audience=enums.STUDENT)
student_events = Topic.objects.create(name="Events", slug="events", sort_order=3, audience=enums.STUDENT)
student_invitations = Topic.objects.create(name="Invitations", slug="invitations", sort_order=4, audience=enums.STUDENT)

# Create FAQ Questions
Question.objects.create(topic=basics_topic, question="What is Umeqo?", slug="what-is-umeqo", answer="Umeqo is a new platform for helping students and employers connect during recruiting season.", status=enums.ACTIVE, audience=enums.ALL, sort_order=0)

# Create Employment Types
new_contents_path = ROOT + "/initial_content/EmploymentTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for type in contents:
    print type
    EmploymentType.objects.create(name=type)
print "Created Employment Types"


# Create Industries
new_contents_path = ROOT + "/initial_content/Industries/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    Industry.objects.create(name=name)
print "Created Industries"


# Create Student Lists 
all_students = StudentList.objects.create(name=student_constants.ALL_STUDENT_GROUP_NAME, sort_order=1, type=student_enums.GENERAL)
all_students.students.add(*list(Student.objects.filter(active=True)))
all_students.employers.add(*list(Employer.objects.filter(subscriber=True)))
print "Created Student Lists"


# Create School Years
new_contents_path = ROOT + "/initial_content/SchoolYears/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    SchoolYear.objects.create(name=name)
print "Created School Years"


# Create Graduation Years
new_contents_path = ROOT + "/initial_content/GraduationYears/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for year in contents:
    print year
    GraduationYear.objects.create(year=year)
print "Created Graduation Years"


# Create Languages
new_contents_path = ROOT + "/initial_content/Languages/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    Language.objects.create(name=name)
print "Created Languages"


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


#Create EventTypes
new_contents_path = ROOT + "/initial_content/EventTypes/"
contents_file = open(new_contents_path + "contents.json")
contents = simplejson.loads(contents_file.read())
for name in contents:
    print name
    EventType.objects.create(name=name)
print "Created Event Types"