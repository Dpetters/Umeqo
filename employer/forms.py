"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from core.choices import NO_YES_CHOICES
from core import choices as core_choices
from core.forms_helper import campus_org_types_as_choices
from student.form_helpers import student_lists_as_choices

from employer.models import FilteringParameters, EmployerPreferences, StudentComment
from employer import enums as employer_enums

class DeliverResumeBookForm(forms.Form):
    delivery_type = forms.ChoiceField(label="Select Delivery Type:", choices = employer_enums.RESUME_BOOK_DELIVERY_CHOICES)
    name = forms.CharField(label="Name Resume Book:", max_length=42, required=False)
    email = forms.EmailField(label="Delivery Email:", required=False)
    
    def __init__(self, *args, **kwargs):
        super(DeliverResumeBookForm, self).__init__(*args, **kwargs)
        print args
        print kwargs
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field', 'placeholder':'Search by keyword, skill, etc..'}))

class FilteringForm(forms.ModelForm):
    gender = forms.ChoiceField(label="Filter by gender:", choices = core_choices.FILTERING_GENDER_CHOICES, initial= core_choices.BOTH_GENDERS, required= False)
    older_than_18 = forms.ChoiceField(label="Must be older than 18:", choices = NO_YES_CHOICES, required = False)

    gpa = forms.DecimalField(label="Minimum GPA:", min_value = 0, max_value = 5, max_digits=5, required = False)
    act = forms.IntegerField(label="Minimum ACT:", max_value = 36, required = False)
    sat_t = forms.IntegerField(label="Minimum SAT:", max_value = 2400, min_value = 600, required = False)
    sat_m = forms.IntegerField(label="Minimum SAT Math:", max_value = 800, min_value = 200, required = False)
    sat_v = forms.IntegerField(label="Minimum SAT Verbal:", max_value = 800, min_value = 200, required = False)
    sat_w = forms.IntegerField(label="Minimum SAT Writing:", max_value = 800, min_value = 200, required = False)

    
    class Meta:
        model = FilteringParameters
        
    def __init__(self, *args, **kwargs):
        super(FilteringForm, self).__init__(*args, **kwargs)
        self.fields['campus_involvement'].choices = campus_org_types_as_choices()

class EmployerPreferencesForm(forms.ModelForm):
    
    class Meta:
        model = EmployerPreferences

class StudentCommentForm(forms.Form):
    comment = forms.CharField(max_length = 500, widget=forms.Textarea(attrs={'class':'student_comment', 'placeholder':'Add Note'}))
    
    class Meta:
        model = StudentComment
        fields = ('comment',)
     
class StudentFilteringForm(FilteringForm):
    ordering = forms.ChoiceField(label="Order Results By:", choices = employer_enums.ORDERING_CHOICES, required = False)
    results_per_page = forms.ChoiceField(label="Results Per Page:", choices = employer_enums.RESULTS_PER_PAGE_CHOICES, required = False)
    
    def __init__(self, *args, **kwargs):
        super(StudentFilteringForm, self).__init__(*args, **kwargs)
        self.fields['student_list'] = forms.ChoiceField(choices = student_lists_as_choices(args[0].get('recruiter', '')))
