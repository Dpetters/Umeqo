from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.utils.translation import ugettext as _

from auth.form_helpers import verify_account

from campus_org.models import CampusOrg
from core import messages as m
from core.email import send_email
from core.form_helpers import decorate_bound_field
from core.models import Language
from employer.models import Recruiter
from registration.models import InterestedPerson

decorate_bound_field()

class BetaForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name:", max_length=42)
    last_name = forms.CharField(label="Last Name:", max_length=42)
    email = forms.EmailField(label="Email:", widget=forms.TextInput(attrs={'placeholder':'e.g. susan@mit.edu'}))
    
    class Meta:
        fields = ('first_name',
                  'last_name',
                  'email')
        model = InterestedPerson
        
class ContactForm(forms.Form):
    name = forms.CharField(label=u'Your Name:', max_length=100, widget=forms.TextInput())
    email = forms.EmailField(label=u'Your Email:', widget=forms.TextInput(attrs=dict(maxlength=200)))
    body = forms.CharField(label=u'Message', widget=forms.Textarea())
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    subject_template_name = "contact_us_form_subject.txt"
    template_name = 'contact_us_email_body.txt'
    _context = None
    
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request
        
    def message(self):
        if callable(self.template_name):
            template_name = self.template_name()
        else:
            template_name = self.template_name
        return loader.render_to_string(template_name, self.get_context())
    
    def subject(self):
        subject = loader.render_to_string(self.subject_template_name, self.get_context())
        return ''.join(subject.splitlines())
    
    def get_context(self):
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        if self._context is None:
            self._context = RequestContext(self.request, dict(self.cleaned_data, site=Site.objects.get_current()))
        return self._context
    
    def get_message_dict(self):
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('message', 'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = callable(attr) and attr() or attr
        return message_dict
    
    def save(self):
        dictionary = self.get_message_dict()
        send_email(dictionary['subject'], dictionary['message'], dictionary['recipient_list'])

class AkismetContactForm(ContactForm):
    def clean(self):
        if 'body' in self.cleaned_data and getattr(settings, 'AKISMET_API_KEY', ''):
            from akismet import Akismet
            from django.utils.encoding import smart_str
            api = Akismet(key=settings.AKISMET_API_KEY, blog_url='http://%s/' % Site.objects.get_current().domain)
            if api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referer': self.request.META.get('HTTP_REFERER', ''),
                                 'user_ip': self.request.META.get('REMOTE_ADDR', ''),
                                 'user_agent': self.request.META.get('HTTP_USER_AGENT', '') }
                if api.comment_check(smart_str(self.cleaned_data['body']), data=akismet_data, build_data=True):
                    raise forms.ValidationError(_(m.contact_us_message_spam))
        return self.cleaned_data

class CreateLanguageForm(forms.ModelForm):
    name = forms.CharField(label="Language:", max_length=42)
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Language.objects.filter(name=name).exists():
            raise forms.ValidationError(_(m.language_already_exists))
        return name
    
    class Meta:
        fields = ('name',)
        model = Language

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email:", max_length = 75)
    
    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': m.email_required}
        self.fields['password'].label = "Password:"
        self.fields['password'].error_messages = {'required': m.password_required}
                
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                pass
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(m.incorrect_username_password_combo)
            
            verify_account(self.user_cache)
            
            if not self.user_cache.is_active:
                self.user_cache.is_active = True
                self.user_cache.save()
        self.check_for_test_cookie()
        return self.cleaned_data

class SuperLoginForm(forms.Form):
    recruiter = forms.ModelChoiceField(label="Recruiter:", queryset = Recruiter.objects.all(), required=False)
    campus_org = forms.ModelChoiceField(label="Campus Org:", queryset = CampusOrg.objects.filter(user__isnull=False), required=False)
    
    def clean(self):
        if not self.cleaned_data.get("recruiter") and not self.cleaned_data.get("campus_org"):
            raise forms.ValidationError("Please pick either a recruiter or campus org.")
        return self.cleaned_data