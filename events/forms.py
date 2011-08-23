from django import forms

from events.models import Event, EventType

from core.form_helpers import decorate_bound_field, boolean_coerce
from core.models import SchoolYear
from core.renderers import RadioSelectTableRenderer
from core.widgets import ImprovedSplitDateTimeWidget
from events.choices import PUBLIC_PRIVATE_BOOLEAN_CHOICES
from ckeditor.widgets import CKEditorWidget

decorate_bound_field()
               
class EventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter event name', 'tabindex':1}))
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), widget=forms.Select(attrs={'tabindex':2}), empty_label="select event type")
    is_public = forms.TypedChoiceField(coerce=boolean_coerce, choices=PUBLIC_PRIVATE_BOOLEAN_CHOICES, initial=True, widget=forms.RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':3}))
    location = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'placeholder':'Enter classroom #, address, etc..', 'tabindex':4}), required=False)
    latitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    description = forms.CharField(widget=CKEditorWidget(attrs={'tabindex':5}))
    start_datetime = forms.DateTimeField(label="Start Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':6}), required=False)
    end_datetime = forms.DateTimeField(label="End Date/Time:", widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':7}))
    audience = forms.ModelMultipleChoiceField(label="Intended Audience:", widget=forms.SelectMultiple(attrs={'tabindex':8}), queryset = SchoolYear.objects.all(), required=False)
    rsvp_message = forms.CharField(label="RSVP Message:", widget=forms.Textarea(attrs={'tabindex':8, 'placeholder':'Tell RSVPs what to wear, bring, etc..'}), required=False)
    
    class Meta:
        fields = ('name', 'start_datetime', 'end_datetime', 'type', 'location', 'latitude', 'longitude', 'audience', 'description', 'rsvp_message', 'is_public',)
        model = Event

class CampusOrgEventForm(EventForm):
    pass