from haystack import indexes, site
from events.models import Event

class EventIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    start_datetime = indexes.DateTimeField(model_attr='start_datetime',null=True)
    end_datetime = indexes.DateTimeField(model_attr='end_datetime')
    type = indexes.CharField(model_attr='type')
    content_auto = indexes.EdgeNgramField(use_template=True)
    privacy = indexes.BooleanField(model_attr='privacy')

site.register(Event, EventIndex)
