"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from models import Topic
from help import enums

def help(request,
         template_name='help.html'):
    
    data = {'topics':[]}
    if hasattr(request.user, "employer"):
        topics = Topic.objects.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.ALL))
    elif hasattr(request.user, "student"):
        topics = Topic.objects.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
    else:
        topics = Topic.objects.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        
    for topic in topics:
        questions = topic.question_set.filter(status = enums.ACTIVE)
        if hasattr(request.user, "employer"):
            questions = topic.question_set.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.ALL))
        elif hasattr(request.user, "student"):
            questions = topic.question_set.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
        else:
            questions = topic.question_set.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        
        data['topics'].append({'name': topic, 'questions':questions})
    
    return render_to_response(template_name,
                              data,
                              context_instance=RequestContext(request))