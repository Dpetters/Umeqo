#import ldap

from django import forms
from django.conf import settings as s
from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage

from student.models import Student, StudentPreferences, StudentInvite, \
                            StudentDeactivation
from campus_org.form_helpers import campus_org_types_as_choices
from campus_org.models import CampusOrg
from core.models import Course, GraduationYear, SchoolYear, EmploymentType, Industry, Language
from core.view_helpers import does_email_exist
from employer.models import Employer
from core.fields import PdfField
from countries.models import Country
from core.choices import SELECT_YES_NO_CHOICES, MONTH_CHOICES
from core import messages as m


class StudentAccountDeactivationForm(forms.ModelForm):
    suggestion = forms.CharField(label="If you still wish to deactivate, \
    please suggest how we can improve:", max_length=16384,
    widget=forms.Textarea, required=False)

    class Meta:
        model = StudentDeactivation
        fields = ['suggestion']
    
class StudentRegistrationForm(forms.Form):

    email = forms.EmailField(label="MIT email:", \
                             widget=forms.TextInput(attrs={'tabindex':1}))
    
    password1 = forms.CharField(label="Password:", \
    widget=forms.PasswordInput(render_value=False, attrs={'tabindex':2}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if does_email_exist(email):
            raise forms.ValidationError(_(m.email_already_registered))
        
        if s.DEBUG:
            if email[-len("mit.edu"):] != "mit.edu" \
            and email[-len("umeqo.com"):] != "umeqo.com":
                raise forms.ValidationError(_(m.must_be_mit_email))
        elif email[-len("mit.edu"):] != "mit.edu":
            raise forms.ValidationError(_(m.must_be_mit_email))
        
        # General idea of what the ldap code below is doing:
        # --Connected to the Internet (dev w/ internet, prod)
        # ----LDAP Up
        # ------Run Student Check, Allow Registration
        # ----LDAP Down
        # ------Send Email Alerting Us
        # ------Do Not Allow Registration
        # --Not Connected to the Internet (dev w/o internet)
        # ----Allow registration. An error will be thrown that the email could
        # ----not be sent, but you can go into the admin and activate the user
        if email[-len("umeqo.com"):] != "umeqo.com":
            # If after ldap check result==[None], then Im not connected to
            # the internet. If result==[], then I am connected and the email
            # is not a student's. 
            res = [None]
            try:
                con = ldap.open('ldap.mit.edu')
                con.simple_bind_s("", "")
                dn = "dc=mit,dc=edu"
                uid = email.split("@")[0]
                res = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])
            except Exception, e:
                try:
                    rcpts = [mail_tuple[1] for mail_tuple in s.MANAGERS]
                    sub = "URGENT: LDAP Server is down. EOM"
                    EmailMessage(sub, "", s.DEFAULT_FROM_EMAIL, rcpts).send()
                    raise forms.ValidationError(_(m.ldap_server_error))
                except:
                    pass
            if not res or (res[0] != None \
                and res[0][1]['eduPersonPrimaryAffiliation'][0] != "student"):
                raise forms.ValidationError(m.must_be_mit_student)
        return self.cleaned_data['email']


class BetaStudentRegistrationForm(StudentRegistrationForm):
    invite_code = forms.CharField(label="Invite Code:", \
                                  widget=forms.TextInput(attrs={'tabindex':2}))
    
    def clean_invite_code(self):
        try:
            StudentInvite.objects.get(id=self.cleaned_data['invite_code'])
        except StudentInvite.DoesNotExist:
            raise forms.ValidationError(m.invalid_invite_code)
        return self.cleaned_data['invite_code']


class StudentEmployerSubscriptionsForm(forms.ModelForm):
    
    class Meta:
        fields = ('subscriptions',)
        model = Student

class StudentUpdateResumeForm(forms.ModelForm):

    resume = PdfField()

    class Meta:
        fields = ('resume',)
        model = Student

class StudentBaseAttributeForm(forms.ModelForm):
    industries_of_interest = forms.ModelMultipleChoiceField(label="Interested in:", \
                            queryset = Industry.objects.all(), required = False)
    
    previous_employers = forms.ModelMultipleChoiceField(label="Previous employers:", \
                            queryset = Employer.objects.all(), required = False)
    
    campus_involvement = forms.ModelMultipleChoiceField(label="Campus involvement:", \
                            queryset = CampusOrg.objects.all(), required = False)
    
    languages = forms.ModelMultipleChoiceField(label="Languages:", \
                            queryset = Language.objects.all(), required = False)
    
    countries_of_citizenship = forms.ModelMultipleChoiceField(label="Countries of citizenship:", \
                            queryset = Country.objects.all(), required=False)
       
    def __init__(self, *args, **kwargs):
        super(StudentBaseAttributeForm, self).__init__(*args, **kwargs)
        self.fields['campus_involvement'].choices = campus_org_types_as_choices()


class StudentProfileForm(StudentBaseAttributeForm):
    # Required Info
    first_name = forms.CharField(label="First name:", max_length = 20)
    last_name = forms.CharField(label="Last name:", max_length = 30)
    school_year = forms.ModelChoiceField(label="School year:", queryset = SchoolYear.objects.all(), empty_label="select school year")
    graduation_year = forms.ModelChoiceField(label="Grad year/month:", queryset = GraduationYear.objects.all().order_by("year"), empty_label="select year")
    graduation_month = forms.ChoiceField(choices = MONTH_CHOICES)
    first_major = forms.ModelChoiceField(label="(First) Major:", queryset = Course.objects.all().order_by('sort_order'), empty_label="select course")
    gpa = forms.DecimalField(label="GPA:", min_value = 0, max_value = 5, max_digits=5, decimal_places=2)
    resume = PdfField(label="Resume:", widget=forms.FileInput(attrs={'class':'required'}))
    
    # Academic Info
    second_major = forms.ModelChoiceField(label="Second major:", queryset = Course.objects.all(), required = False, empty_label = "select course")
    act = forms.ChoiceField(label="ACT:", required = False, choices=[('','---')]+[(x,x) for x in range(36,0,-1)])
    sat_m = forms.ChoiceField(label="SAT Math:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_v = forms.ChoiceField(label="SAT Verbal:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    sat_w = forms.ChoiceField(label="SAT Writing:", required = False, choices=[('','---')]+[(x,x) for x in range(800,190,-10)])
    
    # Work-Related Info
    looking_for = forms.ModelMultipleChoiceField(label="Looking for:", queryset = EmploymentType.objects.all(), required = False)
    
    website = forms.URLField(label="Personal Website:", required=False)
    older_than_21 = forms.ChoiceField(label="Older than 21:", choices = SELECT_YES_NO_CHOICES, required = False)

    class Meta:
        fields = ('first_name',
                   'last_name',
                   'school_year',
                   'graduation_year',
                   'graduation_month',
                   'first_major',
                   'gpa',
                   'resume',
                   'older_than_21',
                   'countries_of_citizenship',
                   'website',
                   'second_major',
                   'sat_m',
                   'sat_v',
                   'sat_w',
                   'act',
                   'campus_involvement',
                   'languages',
                   'looking_for',
                   'previous_employers',
                   'industries_of_interest',
                    )
        model = Student
        
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        if kwargs['instance'].profile_created:
            self.fields['resume'] = PdfField(label="Resume:", required=False)

    # The Django IntegerField does not (but SHOULD) support '' as an empty value
    # Therefore I have to check for '' and return None if it's that.
    # We can't use None in the choices themselves because jquery validation
    # complains that you're not submitting an integer but "None"
    def clean_sat_m(self):
        sat_m = self.cleaned_data["sat_m"]
        if not sat_m:
            return None
        return sat_m

    def clean_sat_w(self):
        sat_w = self.cleaned_data["sat_w"]
        if not sat_w:
            return None
        return sat_w
        
    def clean_sat_v(self):
        sat_v = self.cleaned_data["sat_v"]
        if not sat_v:
            return None
        return sat_v
        
    def clean_act(self):
        act = self.cleaned_data["act"]
        if not act:
            return None
        return act
    
    def clean_second_major(self):
        first_major = self.cleaned_data.get("first_major")
        second_major = self.cleaned_data.get("second_major")
        if first_major and second_major and first_major == second_major:
            raise forms.ValidationError(_(m.first_second_majors_diff))
        return self.cleaned_data['second_major']

class StudentProfilePreviewForm(StudentProfileForm):
    resume = PdfField(label="Resume:", required=False)

class StudentPreferencesForm(forms.ModelForm):

    class Meta:
        fields = ("email_on_invite_to_public_event",
                  "email_on_invite_to_private_event",
                  "email_on_new_subscribed_employer_event" )
        model = StudentPreferences