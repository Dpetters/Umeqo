from datetime import datetime

from employer.models import Employer

from haystack import indexes, site
from django.db.models import Q

class EmployerIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    content_auto = indexes.EdgeNgramField(use_template=True)
    industries = indexes.MultiValueField()
    subscribers = indexes.MultiValueField()
    has_events = indexes.BooleanField()
    visible = indexes.BooleanField(model_attr="visible")

    def prepare_industries(self, obj):
        return [industry.id for industry in obj.industries.all()]
    
    def prepare_has_events(self, obj):
        # First part counts events created by a campus org, second part counts the employer's events
        return obj.event_set.filter(is_public=True).filter(Q(end_datetime__gte=datetime.now().strftime('%Y-%m-%d %H:%M:00')) | Q(type__name="Rolling Deadline")).distinct().count() > 0
    
    def prepare_subscribers(self, obj):
        return [u.user.id for u in obj.subscriptions.all()]

site.register(Employer, EmployerIndex)
