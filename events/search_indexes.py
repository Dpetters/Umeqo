from haystack import indexes, site
from events.models import Event

class EventIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    start_datetime = indexes.DateTimeField(model_attr='start_datetime',null=True)
    end_datetime = indexes.DateTimeField(model_attr='end_datetime', null=True)
    type = indexes.CharField(model_attr='type')
    content_auto = indexes.EdgeNgramField(use_template=True)
    is_public = indexes.BooleanField(model_attr='is_public')

site.register(Event, EventIndex)
