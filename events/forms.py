from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from events.models import Event, EventType
from events.choices import TIME_CHOICES
from core.forms_helper import decorate_bound_field

decorate_bound_field()

class ImprovedSplitDateTimeWidget(forms.MultiWidget):
    """
    Copied from SplitDateTimeWidget, but also adds a class to date and time for js/css customization:
    A Widget that splits datetime input into two <input type="text"> boxes.
    """

    def __init__(self, dateAttrs={'class':'datefield'}, timeAttrs={'class':'timefield'}, date_format=None, time_format=None, initial=None):
        widgets = (forms.DateInput(attrs=dateAttrs, format="%m/%d/%Y"),
                   forms.Select(attrs=timeAttrs, choices=TIME_CHOICES))
        super(ImprovedSplitDateTimeWidget, self).__init__(widgets, {})

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
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter event name'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter classroom #, address, etc..'}))
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), empty_label="select event type",label="Type:")
    is_public = forms.TypedChoiceField(coerce=lambda x: bool(int(x)), choices=((0, 'Public'), (1, 'Private')), widget=forms.RadioSelect(renderer=RadioSelectTableRenderer))
    start_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(),required=False,label="Start Date/Time:")
    end_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(),label="End Date/Time:")
    
    class Meta:
        fields = ('name', 'start_datetime', 'end_datetime', 'type', 'location', 'audience', 'description', 'is_public',)
        model = Event