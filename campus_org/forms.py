from django import forms

from campus_org.models import CampusOrg, CampusOrgPreferences
from core.models import CampusOrgType
from core.form_helpers import decorate_bound_field
from core.view_helpers import employer_campus_org_slug_exists, does_email_exist
from core import messages as m

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

class CampusOrgRegistrationForm(forms.Form):
    email = forms.EmailField(label=".edu Email:", widget=forms.TextInput(attrs={'tabindex':1}))
    password = forms.CharField(label="Choose Password:", widget=forms.PasswordInput(render_value=False, attrs={'tabindex':2}))
    name = forms.CharField(label="Campus Org Name:", max_length=42)
    
    
    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            if CampusOrg.objects.get(name=name).user:
                raise forms.ValidationError("This campus org is already registered.")
        except CampusOrg.DoesNotExist:
            pass
        return name

    def clean_email(self):
          email = self.cleaned_data['email']
          if does_email_exist(email):
               raise forms.ValidationError(m.email_already_registered)
                                                                         
          if email[-len(".edu"):] != ".edu":
               raise forms.ValidationError(m.must_be_edu_email)
          return self.cleaned_data['email']
   
 
class CampusOrgProfileForm(CreateCampusOrganizationForm):
    name = forms.CharField(label="Name:", max_length=42)
    type = forms.ModelChoiceField(label="Type:", queryset = CampusOrgType.objects.all())
    email = forms.EmailField(label="E-mail:", required=False)
    slug = forms.SlugField(label="Short URL:", max_length=42)
    website = forms.URLField(label="Website:", required=False)
    image = forms.ImageField(label="Image:", required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea(), max_length = 1000, required=False)
    
    class Meta:
        fields = ('name',
                  'type',
                  'email',
                  'website',
                  'slug',
                  'image',
                  'description')
        model = CampusOrg
    
    def clean_slug(self):
        if self.cleaned_data['slug']:
            if employer_campus_org_slug_exists(self.cleaned_data['slug'], campusorg=self.instance):
                raise forms.ValidationError(m.slug_already_taken)
        return self.cleaned_data['slug']
    
class CampusOrgPreferencesForm(forms.ModelForm):
    pass
    class Meta:
        fields = ()
        model = CampusOrgPreferences
