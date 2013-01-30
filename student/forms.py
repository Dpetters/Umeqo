import os

from pyPdf import PdfFileReader

from django import forms
from django.conf import settings as s
from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from campus_org.form_helpers import campus_org_types_as_choices
from campus_org.models import CampusOrg
from core import messages as m
from core.choices import SELECT_YES_NO_CHOICES, MONTH_CHOICES
from core.form_helpers import decorate_bound_field
from core.fields import PdfField
from core.model_helpers import get_resume_filename
from core.models import Course, GraduationYear, EmploymentType, Industry, Language, School
from core.view_helpers import does_email_exist
from countries.models import Country
from employer.models import Employer
from registration.models import RegException
from student.models import DegreeProgram, Student, StudentPreferences, StudentDeactivation
from student.view_helpers import extract_resume_keywords

decorate_bound_field()
    
class StudentAccountDeactivationForm(forms.ModelForm):
    suggestion = forms.CharField(label="If you still wish to deactivate, please suggest how we can improve:", max_length=16384, widget=forms.Textarea, required=False)

    class Meta:
        model = StudentDeactivation
        fields = ['suggestion']
      
class StudentRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label=".edu Email:", widget=forms.TextInput(attrs={'tabindex':1}))
    password = forms.CharField(label="Password:", widget=forms.PasswordInput(render_value=False, attrs={'tabindex':2}))

    class Meta:
        fields = ('email', 'password')
        model=User
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if does_email_exist(email):
            raise forms.ValidationError(_(m.email_already_registered))
        
        if s.DEBUG:
            if email[-len(".edu"):] != ".edu" and email[-len("umeqo.com"):] != "umeqo.com":
                raise forms.ValidationError(_(m.must_be_edu_email))
        elif email[-len(".edu"):] != ".edu":
            raise forms.ValidationError(_(m.must_be_edu_email))
        return self.cleaned_data['email']



class StudentEmployerSubscriptionsForm(forms.ModelForm):
    
    class Meta:
        fields = ('subscriptions',)
        model = Student

class StudentUpdateResumeForm(forms.ModelForm):

    resume = PdfField(label="Resume:")

    class Meta:
        fields = ('resume',)
        model = Student

    def clean_resume(self):
        if self.cleaned_data['resume']:
            # Read resume to a file
            resume_file_contents = self.cleaned_data['resume']
            resume_test_file_name = get_resume_filename(self.instance, "")
            resume_file = open("%s%s" % (s.MEDIA_ROOT, resume_test_file_name), "wb")
            resume_file.write(resume_file_contents.read())
            resume_file.close()
            
            # File size check
            if os.path.getsize("%s%s" % (s.MEDIA_ROOT, resume_test_file_name)) > s.MAX_RESUME_SIZE:
                max_resume_size = s.MAX_RESUME_SIZE/1024/1024
                raise forms.ValidationError(_(m.resume_file_size % max_resume_size))
            resume_file = open("%s%s" % (s.MEDIA_ROOT, resume_test_file_name), "rb")
            
            # Check that PdfFileReader can read the file
            try:
                PdfFileReader(resume_file)
            except Exception as e:
                raise forms.ValidationError(_(m.resume_file_problem))
            
            # Check that there are less than 3k keywords
            keywords, num = extract_resume_keywords(resume_test_file_name)
            if num > s.MAX_RESUME_KEYWORDS:
                raise forms.ValidationError(_(m.resume_has_too_many_words))
        return self.cleaned_data['resume']


class StudentBaseAttributeForm(forms.ModelForm):
    industries_of_interest = forms.ModelMultipleChoiceField(label="Interested in:", queryset = Industry.objects.all(), required = False)
    previous_employers = forms.ModelMultipleChoiceField(label="Previous employers:", queryset = Employer.objects.all(), required = False)
    campus_involvement = forms.ModelMultipleChoiceField(label="Campus involvement:", queryset = CampusOrg.objects.all(), required = False)
    languages = forms.ModelMultipleChoiceField(label="Languages:", queryset = Language.objects.all(), required = False)
    countries_of_citizenship = forms.ModelMultipleChoiceField(label="Countries of citizenship:", queryset = Country.objects.all(), required=False)
       
    def __init__(self, *args, **kwargs):
        super(StudentBaseAttributeForm, self).__init__(*args, **kwargs)
        self.fields['campus_involvement'].choices = campus_org_types_as_choices()
        

class StudentProfileBaseForm(StudentUpdateResumeForm):
    first_name = forms.CharField(label="First name:", max_length = 20)
    last_name = forms.CharField(label="Last name:", max_length = 30)
    degree_program = forms.ModelChoiceField(label="Degree Program:", queryset = DegreeProgram.objects.all(), empty_label="select degree program")
    graduation_year = forms.ModelChoiceField(label="Grad year/month:", queryset = GraduationYear.objects.all().order_by("year"), empty_label="select year")
    graduation_month = forms.ChoiceField(choices = MONTH_CHOICES)
    first_major = forms.ModelChoiceField(label="(First) Major:", queryset = Course.objects.all(), empty_label="select major")
    gpa = forms.DecimalField(label="GPA:", min_value = 0, max_value = 5, max_digits=5, decimal_places=2)

    class Meta:
        fields = ('first_name',
                   'last_name',
                   'degree_program',
                   'graduation_year',
                   'graduation_month',
                   'first_major',
                   'gpa',
                   'resume',
                    )
        model=Student


class StudentQuickRegistrationForm(StudentProfileBaseForm, StudentRegistrationForm):
    email = forms.EmailField(label=".edu Email:")
    password = forms.CharField(label="Choose Password:", widget=forms.PasswordInput(render_value=False))
    event_id = forms.CharField(widget=forms.HiddenInput)
    action = forms.CharField(widget=forms.HiddenInput)


class StudentProfileForm(StudentBaseAttributeForm, StudentProfileBaseForm):
    act = forms.ChoiceField(label="ACT:", required = False, choices=[('','---')]+[(x,x) for x in range(36,0,-1)])
    sat_m = forms.ChoiceField(label="SAT Math:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_v = forms.ChoiceField(label="SAT Verbal:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_w = forms.ChoiceField(label="SAT Writing:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    looking_for = forms.ModelMultipleChoiceField(label="Looking for:", queryset = EmploymentType.objects.all(), required = False)
    second_major = forms.ModelChoiceField(label="Second major:", queryset = Course.objects.all(), required = False, empty_label = "select major")
    
    website = forms.URLField(label="Personal Website:", required=False)
    older_than_21 = forms.ChoiceField(label="Older than 21:", choices = SELECT_YES_NO_CHOICES, required = False)

    class Meta:
        fields = ('first_name',
                   'last_name',
                   'degree_program',
                   'graduation_year',
                   'graduation_month',
                   'first_major',
                   'gpa',
                   'resume',
                   'older_than_21',
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
                    )
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        if kwargs['instance'].profile_created:
            self.fields['resume'] = PdfField(label="Resume:", required=False)

    # The Django IntegerField does not (but SHOULD) support '' as an empty value
    # Therefore I have to check for '' and return None if it's that.
    # We can't use None in the choices themselves because jquery validation
    # complains that you're not submitting an integer but "None"
    def clean_sat_m(self):
        sat_m = self.cleaned_data["sat_m"]
        if not sat_m:
            return None
        return sat_m

    def clean_sat_w(self):
        sat_w = self.cleaned_data["sat_w"]
        if not sat_w:
            return None
        return sat_w
        
    def clean_sat_v(self):
        sat_v = self.cleaned_data["sat_v"]
        if not sat_v:
            return None
        return sat_v
        
    def clean_act(self):
        act = self.cleaned_data["act"]
        if not act:
            return None
        return act
    
    def clean_second_major(self):
        first_major = self.cleaned_data.get("first_major")
        second_major = self.cleaned_data.get("second_major")
        if first_major and second_major and first_major == second_major:
            raise forms.ValidationError(_(m.first_second_majors_diff))
        return self.cleaned_data['second_major']

    def clean_languages(self):
        languages = {}
        for language in self.cleaned_data.get("languages"):
            if languages.has_key(language.name):
                raise forms.ValidationError(_(m.one_language_difficulty))
            else:
                languages[language.name] = None
        if len(self.cleaned_data.get("languages")) > s.SP_MAX_LANGUAGES:
            raise forms.ValidationError(_(m.max_languages_exceeded))
        return self.cleaned_data['languages']

    def clean_campus_involvement(self):
        if len(self.cleaned_data.get("campus_involvement")) > s.SP_MAX_CAMPUS_INVOLVEMENT:
            raise forms.ValidationError(_(m.max_campus_involvement_exceeded))
        return self.cleaned_data['campus_involvement']
    
    def clean_previous_employers(self):
        if len(self.cleaned_data.get("previous_employers")) > s.SP_MAX_PREVIOUS_EMPLOYERS:
            raise forms.ValidationError(_(m.max_previous_employers_exceeded))
        return self.cleaned_data['previous_employers']

    def clean_industries_of_interest(self):
        if len(self.cleaned_data.get("industries_of_interest")) > s.SP_MAX_INDUSTRIES_OF_INTEREST:
            raise forms.ValidationError(_(m.max_industries_of_interest_exceeded))
        return self.cleaned_data['industries_of_interest']

    def clean_countries_of_citizenship(self):
        if len(self.cleaned_data.get("countries_of_citizenship")) > s.SP_MAX_COUNTRIES_OF_CITIZENSHIP:
            raise forms.ValidationError(_(m.max_countries_of_citizenship_exceeded))
        return self.cleaned_data['countries_of_citizenship']
    

class StudentProfilePreviewForm(StudentProfileForm):
    resume = PdfField(label="Resume:", required=False)


class StudentPreferencesForm(forms.ModelForm):

    class Meta:
        fields = ("email_on_invite_to_public_event",
                  "email_on_invite_to_private_event",
                  "email_on_new_subscribed_employer_event",
                  "receive_monthly_newsletter" )
        model = StudentPreferences
