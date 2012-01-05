from haystack import indexes, site
from events.models import Event

class EventIndex(indexes.RealTimeSearchIndex):
    text = indexes.EdgeNgramField(use_template=True, document=True)
    start_datetime = indexes.DateTimeField(model_attr='start_datetime',null=True)
    end_datetime = indexes.DateTimeField(model_attr='end_datetime', null=True)
    owner = indexes.CharField(model_attr="owner__id")
    type = indexes.CharField(model_attr='type')
    is_public = indexes.BooleanField(model_attr='is_public')
    is_deadline = indexes.BooleanField(model_attr="is_deadline")
    attending_employers = indexes.MultiValueField()
    archived = indexes.BooleanField(model_attr="archived")
    cancelled = indexes.BooleanField(model_attr="cancelled")
    attendees = indexes.MultiValueField()

    def prepare_looking_for(self, obj):
        return [employer.id for employer in obj.attending_employers.all()]
    
    def prepare_attendees(self, obj):
        return [attendee.student.user.id for attendee in obj.attendee_set.all()]
            

site.register(Event, EventIndex)