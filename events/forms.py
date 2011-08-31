from ckeditor.widgets import CKEditorWidget

from django import forms
from django.utils.translation import ugettext_lazy as _

from core.form_helpers import decorate_bound_field, boolean_coerce
from core.models import SchoolYear
from core.renderers import RadioSelectTableRenderer
from core.widgets import ImprovedSplitDateTimeWidget
from events.choices import PUBLIC_PRIVATE_BOOLEAN_CHOICES, DROP_BOOLEAN_CHOICES
from events.models import Event, EventType
from core import messages as m
from employer.models import Employer

decorate_bound_field()
class EventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter event name', 'tabindex':1}))
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), widget=forms.Select(attrs={'tabindex':2}), empty_label="select event type")
    is_public = forms.TypedChoiceField(coerce=boolean_coerce, choices=PUBLIC_PRIVATE_BOOLEAN_CHOICES, initial=True, widget=forms.RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':3}))
    is_drop = forms.TypedChoiceField(coerce=boolean_coerce, choices=DROP_BOOLEAN_CHOICES, initial=True, widget=forms.RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':4}))
    location = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'placeholder':'Enter classroom #, address, etc..', 'tabindex':5}), required=False)
    latitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    description = forms.CharField(widget=CKEditorWidget(attrs={'tabindex':6}))
    start_datetime = forms.DateTimeField(label="Start Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':7}), required=False)
    end_datetime = forms.DateTimeField(label="End Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':8}), required=False)
    audience = forms.ModelMultipleChoiceField(label="Intended Audience:", widget=forms.SelectMultiple(attrs={'tabindex':9}), queryset = SchoolYear.objects.all(), required=False)
    rsvp_message = forms.CharField(label="RSVP Message:", widget=forms.Textarea(attrs={'tabindex':10, 'placeholder':'Tell RSVPs what to wear, bring, etc..'}), required=False)
    
    class Meta:
        fields = ('name', 
                  'start_datetime', 
                  'end_datetime', 
                  'type', 
                  'is_drop', 
                  'location', 
                  'latitude', 
                  'longitude', 
                  'audience', 
                  'description', 
                  'rsvp_message', 
                  'is_public',)
        model = Event
        
    def clean(self):
        if not self.cleaned_data["type"]==EventType.objects.get(name="Rolling Deadline") and not self.cleaned_data["type"]==EventType.objects.get(name="Hard Deadline"):
            if not self.cleaned_data['start_datetime']:
                raise forms.ValidationError(_(m.start_datetime_required))
        elif not self.cleaned_data["type"]==EventType.objects.get(name="Rolling Deadline"):
            if not self.cleaned_data['end_datetime']:
                raise forms.ValidationError(_(m.end_datetime_required))            
        return self.cleaned_data

class CampusOrgEventForm(EventForm):
    attending_employers = forms.ModelMultipleChoiceField(label="Attending Employers:", widget=forms.SelectMultiple(attrs={'tabindex':9}), queryset = Employer.objects.all(), required=False)
    
    class Meta:
        fields = ('name', 
                  'start_datetime', 
                  'end_datetime', 
                  'type', 
                  'is_drop',
                  'attending_employers',
                  'location', 
                  'latitude', 
                  'longitude', 
                  'audience', 
                  'description', 
                  'rsvp_message',
                  'is_public',)
        model = Event
