"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from student.models import Student
from core.forms_helper import campus_org_types_as_choices
from core.models import Course, GraduationYear, SchoolYear, EmploymentType, Industry, CampusOrg, Language
from employer.models import Employer
from core.fields import PdfField
from core.choices import SELECT_YES_NO_CHOICES

class StudentRegistrationForm(forms.Form):

    email = forms.EmailField(label="Your MIT Email:")
    password1 = forms.CharField(label="Choose a Password:", widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Re-enter Password:", widget=forms.PasswordInput(render_value=False))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

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
         
    """
    Required Info
    """  
    first_name = forms.CharField(label="First Name:", max_length = 20)
    last_name = forms.CharField(label="Last Name:", max_length = 30)
    school_year = forms.ModelChoiceField(label="School Year:", queryset = SchoolYear.objects.all(), empty_label="select school year")
    graduation_year = forms.ModelChoiceField(label="Graduation Year:", queryset = GraduationYear.objects.all().order_by("year"), empty_label="select graduation year")
    first_major = forms.ModelChoiceField(label="First Major:", queryset = Course.objects.all().order_by('sort_order'), empty_label="select course")
    gpa = forms.DecimalField(label="GPA:", min_value = 0, max_value = 5, max_digits=5)
    resume = PdfField(label="Resume:", widget=forms.FileInput(attrs={'class':'required'}))
    
    
    """
        Academic Info
    """
    second_major = forms.ModelChoiceField(label="Second Major:", queryset = Course.objects.all(), required = False, empty_label = "select course")
    act = forms.IntegerField(label="ACT:", max_value = 36, required = False, widget=forms.TextInput(attrs={'class': 'act'}))
    sat_m = forms.IntegerField(label="SAT Math:", max_value = 800, min_value = 200, required = False)
    sat_v = forms.IntegerField(label="SAT Verbal:", max_value = 800, min_value = 200, required = False)
    sat_w = forms.IntegerField(label="SAT Writing:", max_value = 800, min_value = 200, required = False)
    
    """
        Work-Related Info
    """
    looking_for = forms.ModelMultipleChoiceField(label="Looking For:", queryset = EmploymentType.objects.all(), required = False)
    previous_employers = forms.ModelMultipleChoiceField(label="Previous Employers:", queryset = Employer.objects.all(), required = False)
    interested_in = forms.ModelMultipleChoiceField(label="Interested In:", queryset = Industry.objects.all(), required = False)
    
    """
        Miscellaneous Info
    """
    # Campus Orgs
    campus_involvement = forms.ModelMultipleChoiceField(label="Campus Involvement:", queryset = CampusOrg.objects.all(), required = False)
    languages = forms.ModelMultipleChoiceField(label="Languages:", queryset = Language.objects.all(), required = False)
    older_than_18 = forms.ChoiceField(label="Older Than 18:", choices = SELECT_YES_NO_CHOICES, required = False)
    citizen = forms.ChoiceField(label="Citizen:", choices = SELECT_YES_NO_CHOICES, required = False)
    website = forms.URLField(label="Website:", required = False)
    
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
                   'campus_involvement',
                   'languages',
                   'looking_for',
                   'previous_employers',
                   'industries_of_interest')
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(StudentCreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['campus_involvement'].choices = campus_org_types_as_choices()

class StudentEditProfileForm(StudentCreateProfileForm):
    resume = PdfField(label="Resume:", required=False)