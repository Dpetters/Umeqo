from __future__ import division
from __future__ import absolute_import

from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings as s
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from core.view_helpers import employer_campus_org_slug_exists
from core.form_helpers import decorate_bound_field
from core import messages as m
from core.choices import NO_YES_CHOICES
from core.models import Industry, EmploymentType
from student.form_helpers import student_lists_as_choices
from student.forms import StudentBaseAttributeForm
from employer.models import RecruiterPreferences, StudentFilteringParameters, Employer
from core import enums as core_enums
from core.widgets import UmSelectWidget
from employer import enums as employer_enums
from ckeditor.widgets import CKEditorWidget

decorate_bound_field()

class CreateEmployerForm(forms.ModelForm):
    name = forms.CharField(label="Name:", max_length=42)
    industries = forms.ModelMultipleChoiceField(label="Industries:", queryset = Industry.objects.all())
    
    class Meta:
        fields = ('name',
                  'industries')
        model = Employer
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            Employer.objects.get(name=name)
            raise forms.ValidationError("This employer already exists.")
        except Employer.DoesNotExist:
            pass
        return self.cleaned_data['name']

    def clean_industries(self):
        industries = self.cleaned_data['industries']
        if len(industries) > s.EP_MAX_INDUSTRIES:
            raise forms.ValidationError("An employer cannot be in more than 5 industries.")
        return self.cleaned_data['industries']
            
class RecruiterForm(forms.ModelForm):
    email = forms.EmailField(label="Email:", max_length = 75)
    first_name = forms.CharField(label="First Name:", max_length=42, required=True)
    last_name = forms.CharField(label="Last Name:", max_length=42, required=True)
    password1 = forms.CharField(label="Choose Password:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput)
    
    class Meta:
        fields = ('email',
                  'first_name',
                  'last_name')
        model = User

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two passwords don't match."))
        return password2

    def save(self, commit=True):
        user = super(RecruiterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
                
class EmployerProfileForm(forms.ModelForm):
    name = forms.CharField(label="Name:", max_length=42)
    slug = forms.SlugField(label="Short URL:", max_length=42)
    industries = forms.ModelMultipleChoiceField(label="Industries:", queryset=Industry.objects.all())
    description = forms.CharField(widget=CKEditorWidget(attrs={'tabindex':5}))
    main_contact = forms.CharField(label="Main Contact:")
    main_contact_email = forms.EmailField(label="Contact Email:")
    main_contact_phone = USPhoneNumberField(label="Contact Phone #:", required=False)
    offered_job_types = forms.ModelMultipleChoiceField(label="Offered Job Types:", queryset=EmploymentType.objects.all(), required=False)
    careers_website = forms.URLField(label="Careers Website:", required=False)
    
    class Meta:
        fields = ('name',
                  'slug', 
                  'industries',
                   'description',
                   'main_contact',
                   'main_contact_email',
                   'main_contact_phone',
                   'offered_job_types',
                   'careers_website')
        model = Employer
    
    def clean_industries(self):
        if len(self.cleaned_data.get("industries")) > s.EP_MAX_INDUSTRIES:
            raise forms.ValidationError(_(m.max_industries_exceeded))
        return self.cleaned_data['industries']
    
    def clean_slug(self):
        if self.cleaned_data['slug']:
            if employer_campus_org_slug_exists(self.cleaned_data['slug'], employer=self.instance):
                raise forms.ValidationError(m.slug_already_taken)
        return self.cleaned_data['slug']

class DeliverResumeBookForm(forms.Form):
    delivery_type = forms.ChoiceField(label="Select Delivery Type:", choices = core_enums.DELIVERY_CHOICES)
    name = forms.CharField(label="Name Resume Book:", max_length=42, required=False)
    emails = forms.CharField(label="Recipient Emails:", max_length=2000, widget=forms.Textarea(), required=False)
        
class StudentSearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field', 'placeholder':'Search by keyword, skill, etc..'}))
    
class StudentDefaultFilteringParametersForm(StudentBaseAttributeForm):
    older_than_21 = forms.ChoiceField(label="Must be older than 21:", choices = NO_YES_CHOICES, required = False)
    gpa = forms.DecimalField(label="Minimum GPA:", min_value = 0, max_value = 5, max_digits=5, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    act = forms.IntegerField(label="Minimum ACT:", max_value = 36, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_t = forms.IntegerField(label="Minimum SAT:", max_value = 2400, min_value = 600, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_m = forms.IntegerField(label="Minimum SAT Math:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_v = forms.IntegerField(label="Minimum SAT Verbal:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_w = forms.IntegerField(label="Minimum SAT Writing:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)

    class Meta:
        fields = ( 'majors',
                   'school_years',
                   'graduation_years',
                   'gpa',
                   'act',
                   'sat_t',
                   'sat_m',
                   'sat_v',
                   'sat_w',
                   'employment_types',
                   'previous_employers',
                   'industries_of_interest',
                   'campus_involvement',
                   'languages',
                   'countries_of_citizenship',
                   'older_than_21'
                    )
        model = StudentFilteringParameters

class StudentFilteringForm(StudentDefaultFilteringParametersForm):
    ordering = forms.ChoiceField(label="Order Results By:", choices = employer_enums.ORDERING_CHOICES, required = False)
    results_per_page = forms.ChoiceField(label="Results Per Page:", choices = employer_enums.RESULTS_PER_PAGE_CHOICES, required = False)

    def __init__(self, *args, **kwargs):
        super(StudentFilteringForm, self).__init__(*args, **kwargs)
        self.fields['student_list'] = forms.ChoiceField(widget = UmSelectWidget, choices = student_lists_as_choices(kwargs.get('initial').get('recruiter_id', '')))

class RecruiterPreferencesForm(forms.ModelForm):
    default_student_result_ordering = forms.ChoiceField(label="Default Student Result Ordering:", choices = employer_enums.ORDERING_CHOICES, required = False)
    default_student_results_per_page = forms.ChoiceField(label="Default Results Per Page:", choices = employer_enums.RESULTS_PER_PAGE_CHOICES, required = False)
    
    class Meta:
        fields = ("email_on_rsvp_to_public_event",
                  "email_on_rsvp_to_private_event",
                  "default_student_results_per_page",
                  "default_student_result_ordering" )
        model = RecruiterPreferences