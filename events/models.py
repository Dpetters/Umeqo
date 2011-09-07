from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from core import mixins as core_mixins
from core.decorators import is_recruiter, is_campus_org
from core.managers import ActiveManager
from core.models import EventType
from core.view_helpers import english_join
from student.models import Student
from notification import models as notification


class Event(core_mixins.DateCreatedTracking):
    # Required Fields
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    end_datetime = models.DateTimeField()
    type = models.ForeignKey(EventType)
    
    # Won't be used immediately, but might prove useful later to show who
    # modified the event and when they did so.
    edits = models.ManyToManyField("core.Edit", null=True, blank=True)
    
    # Events Created by Campus Orgs will need to know which Employers are coming
    attending_employers = models.ManyToManyField("employer.Employer", null=True, blank=True)

    # Non-Deadline Fields   
    start_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Optional Fields
    audience = models.ManyToManyField("core.SchoolYear", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rsvp_message = models.TextField(blank=True,null=True)

    # Statistics fields for "X new views"
    last_seen_view_count = models.PositiveIntegerField(default=0)  
    view_count = models.PositiveIntegerField(default=0)
    
    slug = models.SlugField(default="event-page")
    
    is_public = models.BooleanField()
    is_active = models.BooleanField(default=True, editable=False)
    is_drop = models.BooleanField()
    
    # manager which returns only active events
    objects = ActiveManager()
    
    def __unicode__(self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('event_page', (), {
            'id': self.id,
            'slug': self.slug,
        })

@receiver(signals.m2m_changed, sender=Event.attending_employers.through)
def send_new_event_notifications(sender, instance, action, reverse, model, pk_set, using, **kwargs):
    if action=="post_add":
        notify_about_event(instance, 'new_event')
                
@receiver(signals.post_save, sender=Event)
def send_cancel_event_notifications(sender, instance, created, raw, **kwargs):
    if not created and not instance.is_active and not raw:
        notify_about_event(instance, 'cancelled_event')

def notify_about_event(instance, notice_type):
    employers = None
    if is_recruiter(instance.owner):
        employers = [instance.owner.recruiter.employer]
    if is_campus_org(instance.owner):
        employers = list(instance.attending_employers.all())
    if employers:
        subscribers = Student.objects.filter(subscriptions__in=employers)
        to_users = list(set(map(lambda n: n.user, subscribers)))
        # Batch the sending by unique groups of subscriptions.
        # This way someone subscribed to A, B, and C gets only one email.
        subscribers_by_user = {}
        employername_table = {}
        for employer in employers:
            employername_table[str(employer.id)] = employer.name
            for to_user in to_users:
                if to_user.id in subscribers_by_user:
                    subscribers_by_user[to_user.id].append(employer.id)
                else:
                    subscribers_by_user[to_user.id] = [employer.id]
        subscription_batches = {}
        for userid,employerids in subscribers_by_user.items():
            key = ':'.join(map(lambda n: str(n), employerids))
            subscription_batches[key] = userid
        for key,userids in subscription_batches.items():
            employer_names = map(lambda n: employername_table[n], key.split(':'))
            has_word = "has" if len(employer_names)==1 else "have"
            employer_names = english_join(employer_names)
            for to_user in to_users:
                print "sending"
                notification.send([to_user], notice_type, {
                    'name': to_user.first_name,
                    'employer_names': employer_names,
                    'has_word': has_word,
                    'event': instance,
                })
        
@receiver(signals.pre_save, sender=Event)
def save_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)

class RSVP(models.Model):
    attending = models.BooleanField(default=True)
    student = models.ForeignKey('student.Student')
    event = models.ForeignKey(Event)
    datetime_created = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (("student", "event"),)

class Invitee(models.Model):
    student = models.ForeignKey(Student, null=True)
    event = models.ForeignKey(Event)
    datetime_created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("student", "event"),)

class Attendee(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200, null=True)
    student = models.ForeignKey(Student, null=True)
    event = models.ForeignKey(Event)
    datetime_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s <%s>' % (self.name, self.email)

    class Meta:
        unique_together = (("student", "event"),)

class DroppedResume(models.Model):
    student = models.ForeignKey(Student, null=True)
    event = models.ForeignKey(Event)
    datetime_created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("student", "event"),)
