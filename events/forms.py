from ckeditor.widgets import CKEditorWidget
from datetime import datetime

from django.forms import Form, ChoiceField, ValidationError, CharField, SelectMultiple, ModelMultipleChoiceField, DateTimeField, Textarea, ModelChoiceField, ModelForm, TextInput, Select, TypedChoiceField, FloatField
from django.forms.widgets import RadioSelect, HiddenInput
from django.utils.translation import ugettext_lazy as _

from core.form_helpers import decorate_bound_field, boolean_coerce
from core.models import SchoolYear
from core.renderers import RadioSelectTableRenderer
from core.widgets import ImprovedSplitDateTimeWidget
from events.choices import PUBLIC_PRIVATE_BOOLEAN_CHOICES, DROP_BOOLEAN_CHOICES, EVENT_TYPE_CHOICES, ALL
from events.models import Event, EventType
from core import messages as m
from core import enums as core_enums
from employer.models import Employer

decorate_bound_field()
class EventForm(ModelForm):
    name = CharField(max_length = 85, widget=TextInput(attrs={'placeholder':'Enter event name', 'tabindex':1}))
    type = ModelChoiceField(queryset = EventType.objects.all(), widget=Select(attrs={'tabindex':2}), empty_label="select event type")
    is_public = TypedChoiceField(coerce=boolean_coerce, choices=PUBLIC_PRIVATE_BOOLEAN_CHOICES, initial=True, widget=RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':3}))
    is_drop = TypedChoiceField(coerce=boolean_coerce, choices=DROP_BOOLEAN_CHOICES, initial=False, widget=RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':4}))
    location = CharField(widget=TextInput(attrs={'autocomplete':'off', 'placeholder':'Enter classroom #, address, etc..', 'tabindex':5}), required=False)
    latitude = FloatField(widget=HiddenInput, required=False)
    longitude = FloatField(widget=HiddenInput, required=False)
    description = CharField(widget=CKEditorWidget(attrs={'tabindex':6}))
    start_datetime = DateTimeField(label="Start Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':7}), required=False)
    end_datetime = DateTimeField(label="End Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':8}), required=False)
    audience = ModelMultipleChoiceField(label="Intended Audience:", widget=SelectMultiple(attrs={'tabindex':9}), queryset = SchoolYear.objects.all(), required=False)
    rsvp_message = CharField(label="RSVP Message:", widget=Textarea(attrs={'tabindex':10, 'placeholder':'Tell RSVPs what to wear, bring, etc..'}), required=False)
    
    class Meta:
        fields = ('name', 
                  'start_datetime', 
                  'end_datetime', 
                  'type',
                  'short_slug',
                  'is_drop', 
                  'location', 
                  'latitude', 
                  'longitude', 
                  'audience', 
                  'description', 
                  'rsvp_message', 
                  'is_public')
        model = Event

    def clean_end_datetime(self):
        if self.cleaned_data['end_datetime'] and self.cleaned_data['end_datetime'] < datetime.now():
            raise ValidationError(_("End date/time must be in the future."))
        return self.cleaned_data['end_datetime']

    def clean(self):
        if not self.cleaned_data["type"]==EventType.objects.get(name="Rolling Deadline") and not self.cleaned_data["type"]==EventType.objects.get(name="Hard Deadline"):
            if not self.cleaned_data['start_datetime']:
                raise ValidationError(_(m.start_datetime_required))
        elif not self.cleaned_data["type"]==EventType.objects.get(name="Rolling Deadline"):
            if not self.cleaned_data['end_datetime']:
                raise ValidationError(_(m.end_datetime_required))
        return self.cleaned_data

class EventFilteringForm(Form):
    query = CharField(widget=TextInput(attrs={'placeholder':"Filter by name, keyword, etc.."}))
    type = ChoiceField(widget=RadioSelect(renderer=RadioSelectTableRenderer), initial=ALL, choices=EVENT_TYPE_CHOICES)
    
class CampusOrgEventForm(EventForm):
    attending_employers = ModelMultipleChoiceField(label="Attending Employers:", widget=SelectMultiple(attrs={'tabindex':9}), queryset = Employer.objects.all(), required=False)

    class Meta:
        fields = ('name', 
                  'start_datetime', 
                  'end_datetime', 
                  'type',
                  'short_slug',
                  'is_drop',
                  'attending_employers',
                  'include_and_more',
                  'location',
                  'latitude',
                  'longitude', 
                  'audience',
                  'description', 
                  'rsvp_message',
                  'is_public',)
        model = Event

class EventExportForm(Form):
    event_id = CharField(max_length = 10, widget=HiddenInput)
    event_list = CharField(max_length=20, widget=HiddenInput)
    export_format = ChoiceField(label="Export Format:", choices = core_enums.EXPORT_CHOICES)
    delivery_type = ChoiceField(label="Delivery Type:", choices = core_enums.DELIVERY_CHOICES)
    emails = CharField(label="Recipient Emails:", max_length=2000, widget=Textarea(), required=False)