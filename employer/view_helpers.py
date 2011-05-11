"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db.models import Q

from notification import models as notification
from haystack.query import SearchQuerySet
from student.models import StudentList
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
    
    
def filter_students(student_list=None, gpa=None, act=None, sat_t=None, sat_m=None, sat_v=None, sat_w=None, citizen=None, older_than_18=None, courses=None):
    kwargs = {}
    
    all_students = StudentList.objects.get(id=student_list).students.all()

    if gpa:
        kwargs['gpa__gte'] = gpa
    if act:
        kwargs['act__gte'] = act
    if sat_t:
        kwargs['sat_t__gte'] = sat_t
    if sat_m:
        kwargs['sat_m__gte'] = sat_m
    if sat_v:
        kwargs['sat_v__gte'] = sat_v
    if sat_w:
        kwargs['sat_w__gte'] = sat_w
    if citizen:
        kwargs['citizen'] = citizen
    if older_than_18:
        kwargs['older_than_18'] = older_than_18
    
    filtering_results = all_students.filter(**kwargs)
    print "Courses " + courses
    if courses:
        filtering_results = filtering_results.filter(Q(first_major__id__in=courses) | Q(second_major__id__in=courses))
    
    return filtering_results


def search_students(query):
    search_query_set = SearchQuerySet().filter(content=query)
    return [result.object for result in search_query_set]
    

def combine_and_order_results(filtering_results, search_results, ordering, query):
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
        if query == "null":
            if ordering == enums.ORDERING_CHOICES[0][0]:
                return filtering_results.order_by('last_updated')
            else:
                return filtering_results.order_by(ordering)
        return []