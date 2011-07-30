from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from core.models import EventType
from core.managers import ActiveManager
from student.models import Student
from notification import models as notification
from employer.models import Employer
from events.choices import EVENT_PRIVACY_CHOICES

class Event(models.Model):
    
    #replaces default objects with a manager that filters out inactive events
    is_active = models.BooleanField(default=True,editable=False)
    objects = ActiveManager()

    # Required Fields
    recruiters = models.ManyToManyField("employer.Recruiter")
    
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
    
    privacy = models.CharField(max_length=2, choices = EVENT_PRIVACY_CHOICES)

    def __unicode__(self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(Event, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('event_page', (), {
            'id': self.id,
            'slug': self.slug,
        })

@receiver(signals.post_save, sender=Event)
def send_new_event_notifications(sender, instance, created, raw, **kwargs):
    if created:
        employers = Employer.objects.filter(recruiter=instance.recruiters.all())
        subscribers = Student.objects.filter(subscriptions__in=employers)
        to_users = map(lambda n: n.user, subscribers)
        employer_names = ", ".join(map(lambda n: n.name, employers))
        has_word = "has" if len(employers)==1 else "have"
        notification.send(to_users, 'new_event', {
            'message': '<strong>%s</strong> %s a new event: "%s"' % (employer_names, has_word, instance.name),
            'permalink': instance.get_absolute_url(),
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
