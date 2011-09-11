from django import forms

from campus_org.models import CampusOrg, CampusOrgPreferences
from core.models import CampusOrgType
from core.form_helpers import decorate_bound_field

decorate_bound_field()


class CreateCampusOrganizationForm(forms.ModelForm):
    name = forms.CharField(label="Name:", max_length=42)
    type = forms.ModelChoiceField(label="Type:", queryset = CampusOrgType.objects.all())
    website = forms.URLField(label="Website:", required = False)
    
    class Meta:
        fields = ('name',
                  'type',
                  'website')
        model = CampusOrg

class CampusOrgProfileForm(CreateCampusOrganizationForm):
    name = forms.CharField(label="Name:", max_length=42)
    type = forms.ModelChoiceField(label="Type:", queryset = CampusOrgType.objects.all())
    email = forms.EmailField(label="E-mail:", required=False)
    website = forms.URLField(label="Website:", required=False)
    image = forms.ImageField(label="Image:", required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea(), max_length = 1000, required=False)
    
    class Meta:
        fields = ('name',
                  'type',
                  'email',
                  'website',
                  'image',
                  'description')
        model = CampusOrg

class CampusOrgPreferencesForm(forms.ModelForm):
    pass
    class Meta:
        fields = ()
        model = CampusOrgPreferences