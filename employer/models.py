"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

from core.models import Industry, CampusOrg, Language, SchoolYear, GraduationYear, Course, UserProfile
from employer.choices import results_per_page, ORDERING_CHOICES

class Employer(UserProfile):
    # Required Info
    company_name = models.CharField("Company Name", max_length = 38, unique = True, help_text="Maximum 41 characters.")
    industries = models.ManyToManyField(Industry) #change to industries
    contact_phone = PhoneNumberField("Contact Phone #")
    
    # Default Filtering Parameters
    automatic_filtering_setup_completed = models.BooleanField(default = False)
    
    older_than_18 = models.BooleanField()
    citizen = models.BooleanField()
    languages = models.ManyToManyField(Language, blank = True, null = True)
    school_years = models.ManyToManyField(SchoolYear, blank = True, null = True)
    graduation_years = models.ManyToManyField(GraduationYear, blank = True, null = True)
    majors = models.ManyToManyField(Course, blank = True, null = True)
    gpa = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null = True)
    looking_for_internship = models.BooleanField()
    looking_for_fulltime = models.BooleanField()
    sat_t = models.PositiveSmallIntegerField(blank = True, null = True)
    sat_m = models.PositiveSmallIntegerField(blank = True, null = True)
    sat_v = models.PositiveSmallIntegerField(blank = True, null = True)
    sat_w = models.PositiveSmallIntegerField(blank = True, null = True)
    act = models.PositiveSmallIntegerField(blank = True, null = True)
    campus_orgs = models.ManyToManyField(CampusOrg, blank = True, null = True)
    previous_employers = models.ManyToManyField('self', blank = True, null=True, symmetrical=False)
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True, related_name="default_industries_of_interest")
    
    # Events and deadlines
    event_subscribers = models.PositiveIntegerField(default = 0)
    events_posted = models.PositiveIntegerField(default = 0)
    
    # Shopping Cart
    students_in_cart = models.ManyToManyField('student.Student', blank = True, null = True, related_name="in_cart_of")
    
    #Statistics
    event_views = models.PositiveIntegerField(default = 0, blank = True, null = True)
    resumes_viewed = models.PositiveIntegerField(default = 0, blank = True, null=True)
    resumes_downloaded = models.PositiveIntegerField(default = 0, blank = True, null = True)
    
    #Default Filtering
    last_seen_students = models.ManyToManyField("student.Student", blank = True, null = True, related_name = "last_seen_by")
    new_students = models.ManyToManyField("student.Student", blank = True, null = True)
    
    # Preferences
    email_on_rsvp = models.BooleanField()
    results_per_page = models.PositiveSmallIntegerField(choices=results_per_page, default=10)
    default_student_ordering = models.CharField(max_length = 42, choices=ORDERING_CHOICES, default=ORDERING_CHOICES[0][0])
    # Meta
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    
    def __unicode__(self):
        return self.company_name