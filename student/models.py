"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models

from core.models import CampusOrg, SchoolYear, GraduationYear, Course, UserProfile, Language, Industry
from core.models_helper import get_resume_filename
from events.models import Event
from student import enums as student_enums


class StudentList(models.Model):
    name = models.CharField("Student List Name", max_length = 42, help_text="Maximum 42 characters.")
    students = models.ManyToManyField("student.Student", blank = True, null = True)
    employers = models.ManyToManyField("employer.Employer", blank = True, null = True)
    type = models.IntegerField(choices=student_enums.STUDENT_GROUP_TYPE_CHOICES)
    sort_order = models.IntegerField("sort order", default=0, help_text='The order you would like the student lists to be displayed.')

    # Meta
    date_created = models.DateTimeField(editable=False, auto_now_add=True)


class Student(UserProfile):

    active = models.BooleanField(default=True)
    
    # Required Info
    first_name = models.CharField(max_length = 20, blank = True, null=True)
    last_name = models.CharField(max_length = 30, blank = True, null=True)
    school_year = models.ForeignKey(SchoolYear, blank = True, null=True)
    graduation_year = models.ForeignKey(GraduationYear, blank = True, null=True)
    first_major = models.ForeignKey(Course, related_name = "first_major", blank = True, null=True)
    gpa = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null=True)
    resume = models.FileField(upload_to = get_resume_filename, blank = True, null=True)
    
    # Basic Info
    older_than_18 = models.BooleanField()
    citizen = models.BooleanField()
    languages = models.ManyToManyField(Language, blank = True, null = True)
    website = models.URLField(blank = True, null=True)
    
    # Academic Info
    second_major = models.ForeignKey(Course, related_name = "second_major", blank = True, null=True)
    sat = models.PositiveSmallIntegerField(blank = True, null=True)
    act = models.PositiveSmallIntegerField(blank = True, null=True)
    
    #On-campus Involvement
    campus_orgs = models.ManyToManyField(CampusOrg, blank = True, null=True)

    # Work Info
    looking_for_internship = models.BooleanField()
    looking_for_fulltime = models.BooleanField()
    previous_employers = models.ManyToManyField("employer.Employer", blank = True, null=True, related_name="previous_employers_of")
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True, related_name="industries_of_interest_of")
    
    # Event Info
    subscribed_employers = models.ManyToManyField("employer.Employer", blank = True, null=True, related_name="subscribed_employers")
    subscribed_industries = models.ManyToManyField(Industry, blank = True, null=True, related_name="subscribed_industries")
    last_seen_events = models.ManyToManyField(Event, blank = True, null=True, related_name = "last_seen_by")
    new_events = models.ManyToManyField(Event, blank = True, null = True)
    
    # Preferences
    email_on_invite_to_public_event = models.BooleanField()
    email_on_invite_to_private_event = models.BooleanField()
    email_on_new_event = models.BooleanField()
    
    # Statistics
    event_invite_count = models.PositiveIntegerField(editable=False, default = 0)
    add_to_resumebook_count = models.PositiveIntegerField(editable=False, default = 0)
    resume_view_count = models.PositiveIntegerField(editable=False, default = 0)
    shown_in_results_count = models.PositiveIntegerField(editable=False, default = 0)
    
    # Metadata
    profile_created = models.BooleanField(default=False)
    last_updated = models.DateTimeField(editable=False, blank = True, null=True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    keywords = models.TextField()

    class Meta:
        verbose_name_plural = "Students"
    
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
  
    def save( self, *args, **kwargs ):
        if self.first_name and self.last_name:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        super(Student, self).save( *args, **kwargs )