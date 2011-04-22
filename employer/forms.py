"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from core.choices import YES_NO_CHOICES
from core.forms_helper import campus_org_types_as_choices
from student.form_helpers import student_lists_as_choices

from employer.models import Employer
from employer import enums


class SearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field'}))

class FilteringForm(forms.ModelForm):
    older_than_18 = forms.ChoiceField(choices = YES_NO_CHOICES, required = False, widget=forms.Select(attrs={'class':"older_than_18"}))
    citizen = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    looking_for_internship = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    looking_for_fulltime = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)

    sat = forms.IntegerField(max_value = 2400, min_value = 600, required = False)
    act = forms.IntegerField(max_value = 36, required = False)
    
    class Meta:
        fields = ('looking_for_internship',
                   'looking_for_fulltime',
                   'older_than_18',
                   'citizen',
                   'school_years',
                   'majors',
                   'graduation_years',
                   'languages',
                   'campus_orgs',
                   'industries_of_interest',
                   'previous_employers',
                   'gpa',
                   'sat',
                   'act')
        model = Employer
        
    def __init__(self, *args, **kwargs):
        super(FilteringForm, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()
    
class StudentFilteringForm(FilteringForm):
    ordering = forms.ChoiceField(choices = enums.ORDERING_CHOICES)
    results_per_page = forms.ChoiceField(choices = enums.RESULTS_PER_PAGE_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super(StudentFilteringForm, self).__init__(*args, **kwargs)
        self.fields['student_list'] = forms.ChoiceField(choices = student_lists_as_choices(args[0].get('employer', '')))