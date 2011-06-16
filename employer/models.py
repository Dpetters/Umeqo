"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User

from student.models import Student
from countries.models import Country
from core.models import Industry, Ethnicity, CampusOrg, Language, SchoolYear, GraduationYear, Course, EmploymentType
from employer import enums as employer_enums
from core import choices as core_choices

        
class ResumeBook(models.Model):
    recruiter = models.OneToOneField("employer.Recruiter")
    file_name = models.CharField(max_length = 100, blank = True, null=True)
    name = models.CharField("Resume Book Name", max_length = 42, blank = True, null = True, help_text="Maximum 42 characters.")
    students = models.ManyToManyField("student.Student", blank = True, null = True)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)


class FilteringParameters(models.Model):
    school_years = models.ManyToManyField(SchoolYear, blank = True, null = True)
    graduation_years = models.ManyToManyField(GraduationYear, blank = True, null = True)
    majors = models.ManyToManyField(Course, blank = True, null = True)
    gpa = models.DecimalField(max_digits = 5, decimal_places = 3, blank = True, null = True)
    sat = models.PositiveSmallIntegerField(blank = True, null = True)
    act = models.PositiveSmallIntegerField(blank = True, null = True)

    previous_employers = models.ManyToManyField('employer.Employer', blank = True, null=True, symmetrical=False)
    industries_of_interest = models.ManyToManyField(Industry, blank = True, null=True, related_name="default_filtering_employers")
    employment_types = models.ManyToManyField(EmploymentType, blank = True, null = True)
    
    campus_involvement = models.ManyToManyField(CampusOrg, blank = True, null = True)
    ethnicities = models.ManyToManyField(Ethnicity, blank = True, null = True)
    languages = models.ManyToManyField(Language, blank = True, null = True)
    gender = models.CharField(max_length=1, choices = core_choices.FILTERING_GENDER_CHOICES, blank = True, null = True)
    older_than_18 = models.CharField(max_length=1, choices = core_choices.NO_YES_CHOICES, blank = True, null = True)
    countries_of_citizenship = models.ManyToManyField(Country, blank=True, null=True)
    
class Recruiter(models.Model):
    
    user = models.OneToOneField(User)
    employer = models.ForeignKey("employer.Employer")
    
    starred_students = models.ManyToManyField("student.Student")
    
    is_active = models.BooleanField(default=True)
    subscribed = models.BooleanField(default=False)
    
    preferences = models.OneToOneField("employer.EmployerPreferences")
    default_filtering_parameters = models.OneToOneField("employer.FilteringParameters", blank = True, null = True)
    statistics = models.OneToOneField("employer.EmployerStatistics")
    
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
        
    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name
    
    def save( self, *args, **kwargs ):
        if not hasattr(self, "preferences"):
            self.preferences = EmployerPreferences.objects.create()
        if not hasattr(self, "default_filtering_parameters"):
            self.default_filtering_parameters = FilteringParameters.objects.create()
        if not hasattr(self, "statistics"):
            self.statistics = EmployerStatistics.objects.create()
        super(Recruiter, self).save( *args, **kwargs )

class StudentComment(models.Model):
    recruiter = models.ForeignKey(Recruiter)
    student = models.OneToOneField(Student)
    comment = models.CharField(max_length=500)
    
class Employer(models.Model): 
    name = models.CharField(max_length = 42, unique = True, help_text="Maximum 42 characters.")
    description = models.CharField(max_length=500, blank=True, default="")
    slug = models.CharField(max_length=20, unique=True, help_text="Maximum 20 characters.")
    
    industries = models.ManyToManyField(Industry)

    main_contact = models.CharField("Main Contact", max_length = 50) 
    main_contact_phone = PhoneNumberField("Contact Phone #")

    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class EmployerPreferences(models.Model):
    email_on_rsvp = models.BooleanField()
    results_per_page = models.PositiveSmallIntegerField(choices=employer_enums.RESULTS_PER_PAGE_CHOICES, default=10)
    default_student_ordering = models.CharField(max_length = 42, choices=employer_enums.ORDERING_CHOICES, default=employer_enums.ORDERING_CHOICES[0][0])

class EmployerStatistics(models.Model):
    resumes_viewed = models.PositiveIntegerField(default = 0, blank = True, null=True)
        