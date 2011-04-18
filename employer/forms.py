"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from core.models import CampusOrg, SchoolYear, GraduationYear, Course, Language, Industry
from core.choices import YES_NO_CHOICES
from core.forms_helper import campus_org_types_as_choices

from employer.models import Employer
from employer.choices import results_per_page, ORDERING_CHOICES


class SearchForm(forms.Form):
    query = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'id':'query_field'}))

class DefaultFilteringParamsForm(forms.ModelForm):
    older_than_18 = forms.ChoiceField(choices = YES_NO_CHOICES, required = False, widget=forms.Select(attrs={'class':"older_than_18"}))
    citizen = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    looking_for_internship = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)
    looking_for_fulltime = forms.ChoiceField(choices = YES_NO_CHOICES, required = False)

    sat_t = forms.IntegerField(max_value = 2400, min_value = 600, required = False)
    sat_m = forms.IntegerField(max_value = 800, min_value = 200, required = False)
    sat_v = forms.IntegerField(max_value = 800, min_value = 200, required = False)
    sat_w = forms.IntegerField(max_value = 800, min_value = 200, required = False)
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
                   'sat_t',
                   'sat_m',
                   'sat_v',
                   'sat_w',
                   'act')
        model = Employer
        
    def __init__(self, *args, **kwargs):
        super(DefaultFilteringParamsForm, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()

class FilteringForm(forms.Form):
    campus_orgs = forms.ModelMultipleChoiceField(queryset = CampusOrg.objects.all())
    school_years = forms.ModelMultipleChoiceField(queryset = SchoolYear.objects.all())
    grad_years = forms.ModelMultipleChoiceField(queryset = GraduationYear.objects.all())
    majors = forms.ModelMultipleChoiceField(queryset = Course.objects.all())
    
    languages = forms.ModelMultipleChoiceField(queryset = Language.objects.all())
    previous_employers = forms.ModelMultipleChoiceField(queryset = Employer.objects.all())
    industries_of_interest = forms.ModelMultipleChoiceField(queryset = Industry.objects.all())
    older_than_18 = forms.ChoiceField(choices = YES_NO_CHOICES)
    citizen = forms.ChoiceField(choices = YES_NO_CHOICES)
    looking_for_internship = forms.ChoiceField(choices = YES_NO_CHOICES)
    looking_for_fulltime = forms.ChoiceField(choices = YES_NO_CHOICES)
        
    ordering = forms.ChoiceField(choices = ORDERING_CHOICES)
    results_per_page = forms.ChoiceField(choices = results_per_page)
    def __init__(self, *args, **kwargs):
        super(FilteringForm, self).__init__(*args, **kwargs)
        self.fields['campus_orgs'].choices = campus_org_types_as_choices()