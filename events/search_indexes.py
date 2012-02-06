from haystack import indexes, site
from events.models import Event

class EventIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    
    start_datetime = indexes.DateTimeField(model_attr='start_datetime',null=True)
    end_datetime = indexes.DateTimeField(model_attr='end_datetime', null=True)
    owner = indexes.CharField(model_attr="owner__id")
    type = indexes.CharField(model_attr='type')
    is_public = indexes.BooleanField(model_attr='is_public')
    is_deadline = indexes.BooleanField(model_attr="is_deadline")
    is_drop = indexes.BooleanField(model_attr="is_drop")
    attending_employers = indexes.MultiValueField()
    archived = indexes.BooleanField(model_attr="archived")
    cancelled = indexes.BooleanField(model_attr="cancelled")
    attendees = indexes.MultiValueField()
    invitees = indexes.MultiValueField()

    def prepare_looking_for(self, obj):
        return [employer.id for employer in obj.attending_employers.all()]

    def prepare_attending_employers(self, obj):
        return [employer.id for employer in obj.attending_employers.all()]
        
    def prepare_attendees(self, obj):
        ids = []
        for attendee in obj.attendee_set.all():
            if attendee.student:
                ids.append(attendee.student.user.id)
        return ids
    
    def prepare_invitees(self, obj):
        return [invitee.student.user.id for invitee in obj.invitee_set.all()]            

site.register(Event, EventIndex)