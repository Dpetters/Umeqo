"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from student.models import Student
from core.forms_helper import campus_org_types_as_choices
from core.models import SchoolYear, GraduationYear, Course
from core.fields import PdfField
from core.choices import YES_NO_CHOICES

class EmployerSubscriptionsForm(forms.ModelForm):
    
    class Meta:
        fields = ('subscribed_employers',)
        model = Student

class ResumeUpdateForm(forms.ModelForm):

    resume = PdfField()

    class Meta:
        fields = ('resume',)
        model = Student

class create_profile_form(forms.ModelForm):
            
    # First Name
    # Last Name
    # Graduation Year
    # First Major
    school_year = forms.ModelChoiceField(queryset = SchoolYear.objects.all(), empty_label="select school year")
    graduation_year = forms.ModelChoiceField(queryset = GraduationYear.objects.all().order_by("year"), empty_label="select graduation year")
    first_major = forms.ModelChoiceField(queryset = Course.objects.all().order_by("name"), empty_label="select course")
    gpa = forms.DecimalField(min_value = 0, max_value = 5, max_digits=5)
    resume = PdfField()
    
   
    # Older than 18
    # Citizen
    website = forms.URLField(required = False)

    second_major = forms.ModelChoiceField(queryset = Course.objects.all(), required = False, empty_label = "select course")
    sat_m = forms.IntegerField(max_value = 800, min_value = 200, required = False)
    sat_v = forms.IntegerField(max_value = 800, min_value = 200, required = False)
    sat_w = forms.IntegerField(max_value = 800, min_value = 200, required = False)
    act = forms.IntegerField(max_value = 36, required = False)
    
    # Campus Orgs
    
    older_than_18 = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    citizen = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    
    looking_for_internship = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    looking_for_fulltime = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    
    # Previous Employers
    # industries_interest
    
    class Meta:
        fields = ('first_name',
                   'last_name',
                   'school_year',
                   'graduation_year',
                   'first_major',
                   'gpa',
                   'resume',
                   'older_than_18',
                   'citizen',
                   'website',
                   'second_major',
                   'sat_m',
                   'sat_v',
                   'sat_w',
                   'act',
                   'campus_orgs',
                   'languages',
                   'looking_for_internship',
                   'looking_for_fulltime',
                   'previous_employers',
                   'industries_of_interest')
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(create_profile_form, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()

class edit_profile_form(create_profile_form):
    resume = PdfField(required=False)