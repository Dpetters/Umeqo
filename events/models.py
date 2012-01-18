from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from core import mixins as core_mixins
from core.models import EventType
from core.view_helpers import um_slugify, english_join
from notification import models as notification
from student.models import Student

class FeaturedEvent(core_mixins.DateCreatedTracking):
    campus_org = models.ForeignKey("campus_org.CampusOrg", null=True, blank=True)
    employer = models.ForeignKey("employer.Employer", null=True, blank=True)
    event = models.ForeignKey("events.Event")    
    
class Event(core_mixins.DateCreatedTracking):
    # Required Fields
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=85)
    end_datetime = models.DateTimeField(null=True, blank=True)
    type = models.ForeignKey(EventType)

    # Won't be used immediately, but might prove useful later to show who
    # modified the event and when they did so.
    edits = models.ManyToManyField("core.Edit", null=True, blank=True)
    
    # Events Created by Campus Orgs will need to know which Employers are coming
    attending_employers = models.ManyToManyField("employer.Employer", null=True, blank=True, related_name="events_attending")
    previously_attending_employers = models.ManyToManyField("employer.Employer", null=True, blank=True)
    
    include_and_more = models.BooleanField(default=False)
    and_more_url = models.URLField(blank=True, null=True)

    # Non-Deadline Fields   
    start_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Optional Fields
    audience = models.ManyToManyField("core.SchoolYear", blank=True, null=True)
    description = models.TextField()
    rsvp_message = models.TextField(blank=True,null=True)
    
    # Statistics fields for "X new views"
    last_seen_view_count = models.PositiveIntegerField(default=0)  
    view_count = models.PositiveIntegerField(default=0)
    
    slug_default = "event-page"
    slug = models.SlugField(default=slug_default)
    short_slug = models.SlugField(blank=True, null=True)
    
    is_public = models.BooleanField()
    cancelled = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    is_drop = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('event_page', (), {
            'id': self.id,
            'slug': self.slug
        })
    
    def save(self):
        if not self.slug or self.slug==self.slug_default:
            self.slug = um_slugify(self.name)
        super(Event, self).save()
    
    def is_deadline(self):
        return self.is_rolling_deadline() or self.type == EventType.objects.get(name='Hard Deadline')
    
    def is_rolling_deadline(self):
        return self.type == EventType.objects.get(name="Rolling Deadline")

def notify_about_event(instance, notice_type, employers):
    subscribers = Student.objects.filter(subscriptions__in=employers)
    to_users = list(set(map(lambda n: n.user, subscribers)))
    if not instance.is_public:
        to_users = filter(lambda u: Invitee.objects.filter(student = u.student, event=instance).exists(), to_users)
    # Batch the sending by unique groups of subscriptions.
    # This way someone subscribed to A, B, and C gets only one email.
    subscribers_by_user = {}
    employername_table = {}
    for employer in employers:
        employername_table[str(employer.id)] = employer.name
        for to_user in to_users:
            if to_user.student in employer.subscribers.all():
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
            notification.send([to_user], notice_type, {
                'name': to_user.first_name,
                'employer_names': employer_names,
                'has_word': has_word,
                'event': instance,
            })
            
@receiver(signals.post_save, sender=Event)
def send_cancel_event_notifications(sender, instance, created, raw, **kwargs):
    if not created and instance.cancelled and not raw:
        notify_about_event(instance, 'cancelled_event', instance.attending_employers.all())


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
    student = models.ForeignKey(Student, null=True, blank=True)
    event = models.ForeignKey(Event)
    datetime_created = models.DateTimeField(auto_now=True)
    won_raffle = models.BooleanField(default=False)

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
