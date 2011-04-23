"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db.models import Q

from notification import models as notification
from haystack.query import SearchQuerySet
from student.models import Student
from employer import enums


def check_for_new_student_matches(employer):
    all_student_matches = filter_students(gpa=employer.gpa,
                                          act=employer.act,
                                          sat = employer.sat)
    latest_student_matches = []
    for student in all_student_matches:
        if student not in employer.last_seen_students.all():
            latest_student_matches.append(student)
            
    employer.latest_student_matches = latest_student_matches
    employer.save()
    
    notification.send([employer.user], 'new_student_matches', {'students':latest_student_matches})
    
    
def filter_students(student_group=None, gpa=None, act=None, sat=None, courses=None):
    kwargs = {}

    all_students = Student.objects.filter(profile_created=True)

    if gpa:
        kwargs['gpa__gte'] = gpa
    if act:
        kwargs['act__gte'] = act
    if sat:
        kwargs['sat__gte'] = sat
    
    filtering_results = all_students.filter(**kwargs)
    
    if courses:
        filtering_results = filtering_results.filter(Q(first_major__name__in=courses) | Q(second_major__name__in=courses))
    
    return filtering_results


def search_students(query):
    search_query_set = SearchQuerySet().filter(content=query)
    return [result.object for result in search_query_set]
    

def order_results(filtering_results, search_results, ordering):
    ordered_results = []
    if search_results:
        if ordering == enums.ORDERING_CHOICES[0][0]:
            for student in search_results:
                if student in filtering_results:
                    ordered_results.append(student)
        else:
            filtering_results.order(ordering)
            for student in filtering_results:
                if student in search_results:
                    ordered_results.append(student)
        return ordered_results
    else:
        if ordering == enums.ORDERING_CHOICES[0][0]:
            return filtering_results.order_by('last_updated')
        else:
            return filtering_results.order_by(ordering)        