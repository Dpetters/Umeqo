"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from core.models import EventType
from core.managers import ActiveManager
    
class Event(models.Model):
    
    #replaces default objects with a manager that filters out inactive events
    is_active = models.BooleanField(default=True,editable=False)
    objects = ActiveManager()

    # Required Fields
    employer = models.ForeignKey("employer.Employer")
    name = models.CharField(max_length=42, unique=True)
    end_datetime = models.DateTimeField()
    type = models.ForeignKey(EventType)

    # Non-Deadline Fields    
    start_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    # Optional Fields
    audience = models.ManyToManyField("core.SchoolYear", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rsvp_message = models.TextField(blank=True,null=True)

    # Statistics fields for "X new views"
    last_seen_view_count = models.PositiveIntegerField(default=0)    
    view_count = models.PositiveIntegerField(default=0)
    
    datetime_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)
