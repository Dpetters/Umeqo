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
from core.choices import SELECT_YES_NO_CHOICES
    
class StudentEmployerSubscriptionsForm(forms.ModelForm):
    
    class Meta:
        fields = ('subscribed_employers',)
        model = Student

class StudentUpdateResumeForm(forms.ModelForm):

    resume = PdfField()

    class Meta:
        fields = ('resume',)
        model = Student

class StudentCreateProfileForm(forms.ModelForm):
            
    # First Name
    # Last Name
    # Graduation Year
    # First Major
    # School Year school_year = forms.ModelChoiceField(queryset = SchoolYear.objects.all(), empty_label="select school year")
    # Graduation Year graduation_year = forms.ModelChoiceField(queryset = GraduationYear.objects.all().order_by("year"), empty_label="select graduation year")
    # First Major first_major = forms.ModelChoiceField(queryset = Course.objects.all().order_by('sort_order'), empty_label="select course")
    #gpa = forms.DecimalField(min_value = 0, max_value = 5, max_digits=5)
    resume = PdfField()
    
   
    # Older than 18
    # Citizen
    website = forms.URLField(required = False)

    second_major = forms.ModelChoiceField(queryset = Course.objects.all(), required = False, empty_label = "select course")
    sat = forms.IntegerField(max_value = 2400, min_value = 600, required = False)
    act = forms.IntegerField(max_value = 36, required = False, widget=forms.TextInput(attrs={'class': 'act'}))
    
    # Campus Orgs
    
    older_than_18 = forms.ChoiceField(choices = SELECT_YES_NO_CHOICES, required = False)
    citizen = forms.ChoiceField(choices = SELECT_YES_NO_CHOICES, required = False)

    # Looking For    
    # Previous Employers
    # Industries of Interest
    
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
                   'sat',
                   'act',
                   'campus_orgs',
                   'languages',
                   'looking_for',
                   'previous_employers',
                   'industries_of_interest')
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(StudentCreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()

class StudentEditProfileForm(StudentCreateProfileForm):
    resume = PdfField(required=False)