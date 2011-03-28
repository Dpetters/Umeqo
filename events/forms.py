"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django import forms

from events.models import Event, EventType, RSVPType
from events.choices import DAY_CHOICES, HOUR_CHOICES, MINUTE_CHOICES

class EventForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset = EventType.objects.all(), empty_label="select event type")
    rsvp_type = forms.ModelChoiceField(queryset = RSVPType.objects.all(), empty_label="select rsvp type", required=False)
    datetime = forms.DateTimeField()
    days = forms.ChoiceField(choices = DAY_CHOICES)
    hours = forms.ChoiceField(choices = HOUR_CHOICES)
    minutes = forms.ChoiceField(choices = MINUTE_CHOICES)
        
    class Meta:
        fields = ('name', 'datetime', 'type', 'rsvp_type', 'external_site', 'email', 'days', 'hours', 'minutes', 'location', 'audience', 'description')
        model = Event