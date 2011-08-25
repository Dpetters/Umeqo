from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.conf import settings as s

from core.form_helpers import decorate_bound_field
from core import messages as m
from core.choices import NO_YES_CHOICES
from core.models import Industry, EmploymentType
from student.form_helpers import student_lists_as_choices
from student.forms import StudentBaseAttributeForm
from employer.models import RecruiterPreferences, StudentFilteringParameters, Employer
from employer import enums as employer_enums
from ckeditor.widgets import CKEditorWidget

decorate_bound_field()

class EmployerProfileForm(forms.ModelForm):
    # Required Fields
    industries = forms.ModelMultipleChoiceField(label="Industries:", queryset=Industry.objects.all())
    description = forms.CharField(widget=CKEditorWidget(attrs={'tabindex':5}))
    main_contact = forms.CharField(label="Main Contact:")
    main_contact_email = forms.EmailField(label="Main Contact Email:")
    
    # Optional Fields
    main_contact_phone = USPhoneNumberField(label="Main Contact Phone #:", required=False)
    offered_job_types = forms.ModelMultipleChoiceField(label="Offered Job Types:", queryset = EmploymentType.objects.all(), required=False)
    website = forms.URLField(label="Careers Website:", required=False)
    
    class Meta:
        fields = ( 'industries',
                   'description',
                   'main_contact',
                   'main_contact_email',
                   'main_contact_phone',
                   'offered_job_types',
                   'website')
        model = Employer
    
    def clean_industries(self):
        if len(self.cleaned_data.get("industries")) > s.EP_MAX_INDUSTRIES:
            raise forms.ValidationError(_(m.max_industries_exceeded))
        return self.cleaned_data['industries']
    

class DeliverResumeBookForm(forms.Form):
    delivery_type = forms.ChoiceField(label="Select Delivery Type:", choices = employer_enums.RESUME_BOOK_DELIVERY_CHOICES)
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
        self.fields['student_list'] = forms.ChoiceField(choices = student_lists_as_choices(kwargs.get('initial').get('employer_id', '')))


class RecruiterPreferencesForm(forms.ModelForm):
    default_student_result_ordering = forms.ChoiceField(label="Default Student Result Ordering:", choices = employer_enums.ORDERING_CHOICES, required = False)
    default_student_results_per_page = forms.ChoiceField(label="Default Results Per Page:", choices = employer_enums.RESULTS_PER_PAGE_CHOICES, required = False)
    
    class Meta:
        fields = ("email_on_rsvp_to_public_event",
                  "email_on_rsvp_to_private_event",
                  "default_student_results_per_page",
                  "default_student_result_ordering" )
        model = RecruiterPreferences