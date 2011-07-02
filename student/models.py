"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from countries.models import Country
from core.models import CampusOrg, SchoolYear, GraduationYear, Course, Language, Industry, EmploymentType, Ethnicity
from core.models_helper import get_resume_filename
from core import choices as core_choices

class Student(models.Model):
    
    user = models.OneToOneField(User)
    
    # Account Info
    profile_created = models.BooleanField(default=False)
    
    # Extracted from resumes
    keywords = models.TextField(blank=True, null=True)
    
    # Required Info
    first_name = models.CharField(max_length = 20, blank = True, null=True)
    last_name = models.CharField(max_length = 30, blank = True, null=True)
    school_year = models.ForeignKey(SchoolYear, blank = True, null=True)
    graduation_year = models.ForeignKey(GraduationYear, blank = True, null=True)
    first_major = models.ForeignKey(Course, related_name = "first_major", blank = True, null=True)
    gpa = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null=True)
    resume = models.FileField(upload_to = get_resume_filename, blank = True, null=True)
    
    # Academic Info
    second_major = models.ForeignKey(Course, related_name = "second_major", blank = True, null=True)
    sat_t = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_m = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_v = models.PositiveSmallIntegerField(blank = True, null=True)
    sat_w = models.PositiveSmallIntegerField(blank = True, null=True)
    act = models.PositiveSmallIntegerField(blank = True, null=True)
    
    # Work Info
    looking_for = models.ManyToManyField(EmploymentType, blank = True, null=True) 
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True, related_name="industries_of_interest_of")
    previous_employers = models.ManyToManyField("employer.Employer", blank = True, null=True, related_name="previous_employers_of")

    # Miscellaneous Info
    campus_involvement = models.ManyToManyField(CampusOrg, blank = True, null=True)
    languages = models.ManyToManyField(Language, blank = True, null = True)
    website = models.URLField(verify_exists=False, blank = True, null=True)
    gender = models.CharField(max_length=1, choices = core_choices.GENDER_CHOICES, blank = True, null = True)
    older_than_18 = models.CharField(max_length=1, choices = core_choices.SELECT_YES_NO_CHOICES, blank = True, null = True)
    ethnicity = models.ForeignKey(Ethnicity, blank = True, null = True)
    countries_of_citizenship = models.ManyToManyField(Country, blank=True, null=True)
    
    # Subscriptions
    subscribed_employers = models.ManyToManyField("employer.Employer", blank = True, null=True, related_name="subscribed_employers")

    is_active = models.BooleanField(default=True)
    preferences = models.OneToOneField("student.StudentPreferences")
    statistics = models.OneToOneField("student.StudentStatistics")
    
    # Dates
    last_updated = models.DateTimeField(editable=False, blank = True, null=True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        verbose_name_plural = "Students"
    
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
  
    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        try:
            self.preferences
        except ObjectDoesNotExist:
            self.preferences = StudentPreferences.objects.create()
        try:
            self.statistics
        except ObjectDoesNotExist:
            self.statistics = StudentStatistics.objects.create()
        super(Student, self).save(*args, **kwargs)

class StudentPreferences(models.Model):
    email_on_invite_to_public_event = models.BooleanField()
    email_on_invite_to_private_event = models.BooleanField()
    email_on_new_event = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Student Preferences"
    
    def __unicode__(self):
        return self.user
  
class StudentStatistics(models.Model):
    event_invite_count = models.PositiveIntegerField(editable=False, default = 0)
    add_to_resumebook_count = models.PositiveIntegerField(editable=False, default = 0)
    resume_view_count = models.PositiveIntegerField(editable=False, default = 0)
    shown_in_results_count = models.PositiveIntegerField(editable=False, default = 0)
