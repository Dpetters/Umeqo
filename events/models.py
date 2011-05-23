"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import EventType
from core.managers import ActiveManager
    
class Event(models.Model):
    
    #replaces default objects with a manager that filters out inactive events
    is_active = models.BooleanField(default=True,editable=False)
    objects = ActiveManager()


    # Required Fields
    employer_user = models.ManyToManyField("employer.EmployerUser")
    
    # Foreign Key to Campus Organization
    
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
    slug = models.SlugField(default="event-page")
    
    rsvps = models.ManyToManyField('student.Student',null=True)
    rsvp_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)

@receiver(signals.pre_save, sender=Event)
def save_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

@receiver(signals.m2m_changed, sender=Event.rsvps.through)
def update_rsvp_count(sender, **kwargs):
    supported = {
        'post_add': 1,
        'post_remove': -1
    }
    action = kwargs['action']
    instance = kwargs['instance']
    pk_set = kwargs['pk_set']
    if action in supported:
        instance.rsvp_count += supported[action]*len(pk_set)
