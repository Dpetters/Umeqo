"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
from django.utils.simplejson import JSONEncoder

from student.models import Student

class ModelAwareJSONEncoder(JSONEncoder):
        
    def default(self, o):
        if isinstance(o, Student):
            return o.__json__()
        return JSONEncoder.default(self, o)
