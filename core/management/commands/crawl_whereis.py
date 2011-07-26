import string
from urllib2 import URLError, urlopen

from django.utils import simplejson
from core.models import Location


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:        
            for char in "%s%s" % (string.ascii_lowercase, string.digits):
                print char
                suggestions_url = "http://whereis.mit.edu/search?q=%s&type=suggest&output=json" % (char)
                for keyword in simplejson.load(urlopen(suggestions_url)):
                    search_url = "http://whereis.mit.edu/search?type=query&q=%s" % (keyword)
                    search_results = simplejson.load(urlopen(search_url))
                    for result in search_results:
                        if not Location.objects.filter(name=result['name']).exists():
                            location = Location.objects.create(name=result['name'], keywords="", latitude = result['lat_wgs84'], longitude=result['long_wgs84'])
                            location.keywords = "%s %s" % (location.keywords, keyword)
                            if result.has_key("displayname") and result["displayname"] != "None":
                                location.display_name = result['displayname']
                            if result.has_key("bldgnum") and result["bldgnum"] != "None":
                                location.building_num = result['bldgnum']
                            if result.has_key("bldgimg") and result["bldgimg"] != "None":
                                location.image_url = result['bldgimg']
                            if result.has_key('contents') and result['contents'] != "None":
                                for content in result['contents']:
                                    if content.has_key('name') and content['name'] != "None":
                                        location.keywords = "%s %s" % (location.keywords, content['name'])
                            location.save()
        except URLError, e:
            print "Error: %s" % (e)
        