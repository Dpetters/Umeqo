"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from core.choices import NO_YES_CHOICES
from core.forms_helper import campus_org_types_as_choices
from student.form_helpers import student_lists_as_choices

from employer.models import FilteringParameters
from employer import enums


class SearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field'}))

class FilteringForm(forms.ModelForm):
    
    older_than_18 = forms.ChoiceField(choices = NO_YES_CHOICES, required = False)
    citizen = forms.ChoiceField(choices = NO_YES_CHOICES, required = False)

    sat = forms.IntegerField(max_value = 2400, min_value = 600, required = False)
    act = forms.IntegerField(max_value = 36, required = False)
    gpa = forms.DecimalField(min_value = 0, max_value = 5, max_digits=5)
    
    class Meta:
        model = FilteringParameters
        
    def __init__(self, *args, **kwargs):
        super(FilteringForm, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()
    
class StudentFilteringForm(FilteringForm):
    ordering = forms.ChoiceField(choices = enums.ORDERING_CHOICES)
    results_per_page = forms.ChoiceField(choices = enums.RESULTS_PER_PAGE_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super(StudentFilteringForm, self).__init__(*args, **kwargs)
        self.fields['student_list'] = forms.ChoiceField(choices = student_lists_as_choices(args[0].get('employer', '')))