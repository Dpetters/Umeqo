from django import forms

from core.choices import NO_YES_CHOICES
from student.form_helpers import student_lists_as_choices
from student.forms import StudentBaseAttributeForm

from employer.models import RecruiterPreferences, FilteringParams
from employer import enums as employer_enums

class DeliverResumeBookForm(forms.Form):
    delivery_type = forms.ChoiceField(label="Select Delivery Type:", choices = employer_enums.RESUME_BOOK_DELIVERY_CHOICES)
    name = forms.CharField(label="Name Resume Book:", max_length=42, required=False)
    emails = forms.CharField(label="Recipient Emails:", max_length=2000, widget=forms.Textarea(), required=False)
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field', 'placeholder':'Search by keyword, skill, etc..'}))

class RecruiterPreferencesForm(forms.ModelForm):
    
    class Meta:
        model = RecruiterPreferences

class FilteringParamsForm(StudentBaseAttributeForm):
    older_than_21 = forms.ChoiceField(label="Must be older than 21:", choices = NO_YES_CHOICES, required = False)

    gpa = forms.DecimalField(label="Minimum GPA:", min_value = 0, max_value = 5, max_digits=5, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    act = forms.IntegerField(label="Minimum ACT:", max_value = 36, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_t = forms.IntegerField(label="Minimum SAT:", max_value = 2400, min_value = 600, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_m = forms.IntegerField(label="Minimum SAT Math:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_v = forms.IntegerField(label="Minimum SAT Verbal:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
    sat_w = forms.IntegerField(label="Minimum SAT Writing:", max_value = 800, min_value = 200, widget=forms.TextInput(attrs={'disabled':'disabled'}), required = False)
        
    class Meta:
        model = FilteringParams
    
    
class StudentFilteringForm(FilteringParamsForm):
    ordering = forms.ChoiceField(label="Order Results By:", choices = employer_enums.ORDERING_CHOICES, required = False)
    results_per_page = forms.ChoiceField(label="Results Per Page:", choices = employer_enums.RESULTS_PER_PAGE_CHOICES, required = False)

    def __init__(self, *args, **kwargs):
        super(StudentFilteringForm, self).__init__(*args, **kwargs)
        self.fields['student_list'] = forms.ChoiceField(choices = student_lists_as_choices(args[0].get('recruiter', '')))
