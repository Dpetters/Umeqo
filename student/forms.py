"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
from django import forms

from student.models import Student, StudentPreferences
from core.forms_helper import campus_org_types_as_choices
from core.models import Course, Ethnicity, GraduationYear, SchoolYear, EmploymentType, Industry, CampusOrg, Language
from core.view_helpers import does_email_exist
from employer.models import Employer
from django.utils.translation import ugettext as _
from core.fields import PdfField
from countries.models import Country
from core.choices import SELECT_YES_NO_CHOICES, GENDER_CHOICES
from core import messages

class StudentRegistrationForm(forms.Form):

    email = forms.EmailField(label="MIT email:")
    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput(render_value=False))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if does_email_exist(email):
            raise forms.ValidationError(_(messages.email_already_registered))
        
        if email[-len("mit.edu"):] != "mit.edu":
            raise forms.ValidationError(_(messages.use_an_mit_email_address))
        """
        con = ldap.open('ldap.mit.edu')
        con.simple_bind_s("", "")
        dn = "dc=mit,dc=edu"
        fields = ['cn', 'sn', 'givenName', 'mail', ]
        username = email.split("@")[0]
        result = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+username, fields)
        if result == []:
            raise forms.ValidationError(_(messages.not_an_mit_student))
        """
        return self.cleaned_data['email']

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
    # Required Info
    first_name = forms.CharField(label="First name:", max_length = 20)
    last_name = forms.CharField(label="Last name:", max_length = 30)
    school_year = forms.ModelChoiceField(label="School year:", queryset = SchoolYear.objects.all(), empty_label="select school year")
    graduation_year = forms.ModelChoiceField(label="Graduation year:", queryset = GraduationYear.objects.all().order_by("year"), empty_label="select graduation year")
    first_major = forms.ModelChoiceField(label="(First) Major:", queryset = Course.objects.all().order_by('sort_order'), empty_label="select course")
    gpa = forms.DecimalField(label="GPA:", min_value = 0, max_value = 5, max_digits=5, decimal_places=2)
    resume = PdfField(label="Resume:", widget=forms.FileInput(attrs={'class':'required'}))
    
    # Academic Info
    second_major = forms.ModelChoiceField(label="Second major:", queryset = Course.objects.all(), required = False, empty_label = "select course")
    #minor = forms.ModelChoiceField(label="Minor:", queryset = Course.objects.all(), required = False, empty_label = "select course")
    act = forms.ChoiceField(label="ACT:", required = False, choices=[('','--')]+[(x,x) for x in range(36,0,-1)])
    sat_m = forms.ChoiceField(label="SAT Math:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_v = forms.ChoiceField(label="SAT Verbal:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_w = forms.ChoiceField(label="SAT Writing:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    
    # Work-Related Info
    looking_for = forms.ModelMultipleChoiceField(label="Looking for:", queryset = EmploymentType.objects.all(), required = False)
    industries_of_interest = forms.ModelMultipleChoiceField(label="Interested in:", queryset = Industry.objects.all(), required = False)
    previous_employers = forms.ModelMultipleChoiceField(label="Previous employers:", queryset = Employer.objects.all(), required = False)
    
    # Miscellaneous Info
    # Campus Orgs
    campus_involvement = forms.ModelMultipleChoiceField(label="Campus involvement:", queryset = CampusOrg.objects.all(), required = False)
    languages = forms.ModelMultipleChoiceField(label="Languages:", queryset = Language.objects.all(), required = False)
    website = forms.URLField(label="Website:", required = False)
    countries_of_citizenship = forms.ModelMultipleChoiceField(label="Countries of citizenship:", queryset = Country.objects.all(), required=False)
    gender = forms.ChoiceField(label="Gender:", choices = GENDER_CHOICES, required=False)
    older_than_18 = forms.ChoiceField(label="Older than 18:", choices = SELECT_YES_NO_CHOICES, required = False)
    ethnicity = forms.ModelChoiceField(label="Ethnicity:", queryset = Ethnicity.objects.all(), empty_label="select ethnicity", required=False)

    class Meta:
        fields = ('first_name',
                   'last_name',
                   'school_year',
                   'graduation_year',
                   'first_major',
                   'gpa',
                   'resume',
                   'older_than_18',
                   'countries_of_citizenship',
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
                   'industries_of_interest',
                   'gender',
                   'ethnicity')
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(StudentCreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['campus_involvement'].choices = campus_org_types_as_choices()
    
    def clean(self):
        first_major = self.cleaned_data.get("first_major")
        second_major = self.cleaned_data.get("second_major")
        if first_major and second_major and first_major == second_major:
            raise forms.ValidationError(_(messages.first_and_second_major_must_be_diff))
        return self.cleaned_data

class StudentEditProfileForm(StudentCreateProfileForm):
    resume = PdfField(label="Resume:", required=False)

class StudentPreferencesForm(forms.ModelForm):

    class Meta:
        fields = ("email_on_invite_to_public_event",
                  "email_on_invite_to_private_event",
                  "email_on_new_event" )
        model = StudentPreferences