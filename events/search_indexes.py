"""
 Developers : Joshua Ma,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from haystack import indexes, site
from events.models import Event

class EventIndex(indexes.RealTimeSearchIndex):
    text = indexes.EdgeNgramField(use_template=True, document=True)
    start_datetime = indexes.DateTimeField(model_attr='start_datetime',null=True)
    end_datetime = indexes.DateTimeField(model_attr='end_datetime')
    type = indexes.CharField(model_attr='type')

site.register(Event, EventIndex)