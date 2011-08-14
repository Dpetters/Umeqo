from haystack import indexes, site
from core.models import Location

class LocationIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)

site.register(Location, LocationIndex)