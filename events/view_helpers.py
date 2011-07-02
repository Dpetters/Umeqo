from datetime import datetime
from events.models import Event
from haystack.query import SearchQuerySet

def event_search_helper(query):
    search_results = SearchQuerySet().models(Event).filter(end_datetime__gte=datetime.now()).order_by("start_datetime")
    if query!="":
        for q in query.split(' '):
            if q.strip() != "":
                search_results = search_results.filter(content_auto=q)
    return search_results
