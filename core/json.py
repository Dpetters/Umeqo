from django.utils.simplejson import JSONEncoder

from student.models import Student

class ModelAwareJSONEncoder(JSONEncoder):
        
    def default(self, o):
        if isinstance(o, Student):
            return o.__json__()
        return JSONEncoder.default(self, o)
