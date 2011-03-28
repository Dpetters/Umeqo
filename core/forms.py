"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django import forms

from core.models import CampusOrg, Language

class CreateCampusOrganizationForm(forms.ModelForm):
    class Meta:
        fields = ('name',
                  'type',
                  'website')
        model = CampusOrg
        
class CreateLanguageForm(forms.ModelForm):
    
    name = forms.CharField(max_length=28)
    
    class Meta:
        fields = ('name',)
        model = Language