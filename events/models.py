"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db import models

class RSVPType(models.Model):
    name = models.CharField(max_length=42, unique=True, help_text="Maximum 41 characters")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(RSVPType, self).save(*args, **kwargs)
        
class EventType(models.Model):
    name = models.CharField("Event Type", max_length = 42, unique = True, help_text="Maximum 41 characters.")
    last_updated = models.DateTimeField(auto_now = True)
    date_created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(EventType, self).save(*args, **kwargs)
    
class Event(models.Model):
    employer = models.ForeignKey("employer.Employer")
    
    name = models.CharField(max_length=42, unique=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank= True, null= True)
    type = models.ForeignKey(EventType)
    location = models.CharField(max_length = 200, blank = True, null = True)
    audience = models.ManyToManyField("core.SchoolYear", blank = True, null = True)
    description = models.TextField(blank=True, null = True)
    rsvps = models.ManyToManyField("student.Student", blank = True, null = True)
    last_seen_rsvps = models.ManyToManyField("student.Student", blank = True, null = True, related_name = "last_rsvped_to")
    view_count = models.PositiveIntegerField(default = 0)
    last_seen_view_count = models.PositiveIntegerField(default = 0)
    
    datetime_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)