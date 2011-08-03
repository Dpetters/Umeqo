from campus_org.models import CampusOrg
from core.models import CampusOrgType
from django import forms

class CreateCampusOrganizationForm(forms.ModelForm):
    name = forms.CharField(label="Name:", max_length=42)
    type = forms.ModelChoiceField(label="Type:", queryset = CampusOrgType.objects.all())
    website = forms.URLField(label="Website:", required = False)
    
    class Meta:
        fields = ('name',
                  'type',
                  'website')
        model = CampusOrg