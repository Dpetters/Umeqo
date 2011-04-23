"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from events.models import Event, EventType, RSVPType
from events.choices import TIME_CHOICES

import copy

class ImprovedSplitDateTimeWidget(forms.MultiWidget):
    """
    Copied from SplitDateTimeWidget, but also adds a class to date and time for js/css customization:
    A Widget that splits datetime input into two <input type="text"> boxes.
    """
    date_format = forms.DateInput.format
    time_format = forms.TimeInput.format

    def __init__(self, dateAttrs={'class':'datefield'}, timeAttrs={'class':'timefield'}, date_format=None, time_format=None):   
        widgets = (forms.DateInput(attrs=dateAttrs, format=date_format),
                   forms.Select(attrs=timeAttrs, choices=TIME_CHOICES))
        super(ImprovedSplitDateTimeWidget, self).__init__(widgets, {})

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
        
    class Media:
        css = {
            'all': ('css/datetime_field.css',),
        }
        js = ('javascript/datetime_field.js',)

class EventForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), empty_label="select event type")
    rsvp_type = forms.ModelChoiceField(queryset = RSVPType.objects.all(), empty_label="select RSVP type", required=False)
    start_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget())
    end_datetime = forms.DateTimeField(widget=ImprovedSplitDateTimeWidget(), required=False)

    class Meta:
        fields = ('name', 'start_datetime', 'end_datetime', 'type', 'location', 'audience', 'description')
        model = Event