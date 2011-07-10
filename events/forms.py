"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from events.models import Event, EventType
from events.choices import TIME_CHOICES
from datetime import datetime

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

BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))
class EventForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), empty_label="select event type",label="Type:")
    start_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(),required=False,label="Start Date/Time:")
    end_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(),label="End Date/Time:")
    is_public = forms.BooleanField(label="Public:", required=False, initial=True)
    
    def __init__(self, *args, **kwargs):
        super(EventForm,self).__init__(*args,**kwargs)
        self.fields['name'].label += ':'
        self.fields['location'].label += ':'
        self.fields['audience'].label += ':'
        self.fields['description'].label += ':'

    class Meta:
        fields = ('name', 'start_datetime', 'end_datetime', 'type', 'location', 'audience', 'description', 'is_public',)
        model = Event
