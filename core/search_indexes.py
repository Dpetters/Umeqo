from haystack import indexes, site
from core.models import Location

class LocationIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(use_template=True, document=True)
    content_auto = indexes.EdgeNgramField(use_template=True)
    building_num = indexes.CharField(model_attr="building_num", null=True)
    
site.register(Location, LocationIndex)