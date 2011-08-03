from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from events.models import Event, EventType
from events.choices import TIME_CHOICES
from core.forms_helper import decorate_bound_field
from core.models import SchoolYear

decorate_bound_field()

class ImprovedSplitDateTimeWidget(forms.MultiWidget):
    """
    Copied from SplitDateTimeWidget, but also adds a class to date and time for js/css customization:
    A Widget that splits datetime input into two <input type="text"> boxes.
    """

    def __init__(self, attrs, dateAttrs={'class':'datefield'}, timeAttrs={'class':'timefield'}, date_format=None, time_format=None, initial=None):
        widgets = (forms.DateInput(attrs=dateAttrs, format="%m/%d/%Y"),
                   forms.Select(attrs=timeAttrs, choices=TIME_CHOICES))
        super(ImprovedSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            thedate = value.date()
            thetime = value.time().replace(minute=(value.minute/30)*30).strftime("%H:%M")
            return [thedate, thetime]
        return [None, None]
        
    class Media:
        css = {
            'all': ('css/datetime_field.css',),
        }

class RadioSelectTableRenderer( RadioFieldRenderer):
    def render( self ):
        """Outputs a series of <td></td> fields for this set of radio fields."""
        return( mark_safe( u''.join( [ u'<td>%s</td>' % force_unicode(w) for w in self ] )))
    
class EventForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter event name', 'tabindex':1}))
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), widget=forms.Select(attrs={'tabindex':2}), empty_label="select event type", label="Type:")
    is_public = forms.TypedChoiceField(coerce=lambda x: bool(int(x)), initial=0, choices=((0, 'Public'), (1, 'Private')), widget=forms.RadioSelect(renderer=RadioSelectTableRenderer, attrs={'tabindex':3}))
    location = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off', 'placeholder':'Enter classroom #, address, etc..', 'tabindex':4}))
    latitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    longitude = forms.FloatField(widget=forms.widgets.HiddenInput, required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'tabindex':5}))
    start_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':6}),required=False, label="Start Date/Time:")
    end_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(attrs={'tabindex':7}),label="End Date/Time:")
    audience = forms.ModelMultipleChoiceField(label="Intended Audience:", widget=forms.SelectMultiple(attrs={'tabindex':8}), queryset = SchoolYear.objects.all(), required=False)
    rsvp_message = forms.CharField(label="RSVP Message:", widget=forms.Textarea(attrs={'tabindex':8, 'placeholder':'Tell RSVPs what to wear, bring, etc..'}), required=False)
    
    class Meta:
        fields = ('name', 'start_datetime', 'end_datetime', 'type', 'location', 'latitude', 'longitude', 'audience', 'description', 'rsvp_message', 'is_public',)
        model = Event