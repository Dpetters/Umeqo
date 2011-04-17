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
        print 0
        print topics
    elif hasattr(request.user, "student"):
        topics = Topic.objects.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
        print 1
        print topics
    else:
        topics = Topic.objects.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
        print 2
        print topics
        
    for topic in topics:
        questions = topic.question_set.filter(status = enums.ACTIVE)
        if hasattr(request.user, "employer"):
            questions = topic.question_set.filter(Q(audience=enums.EMPLOYER) | Q(audience=enums.ALL))
            print 3
            print questions
        elif hasattr(request.user, "student"):
            questions = topic.question_set.filter(Q(audience=enums.STUDENT) | Q(audience=enums.ALL))
            print 4
            print topic.question_set.all()
            print questions
        else:
            questions = topic.question_set.filter(Q(audience=enums.ANONYMOUS) | Q(audience=enums.ALL))
            print 5
            print questions
        data['topics'].append({'name': topic, 'questions':questions})
    return render_to_response(template_name,
                              data,
                              context_instance=RequestContext(request))