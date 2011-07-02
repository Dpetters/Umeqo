"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.db.models import Q
from django.core.cache import cache

from notification import models as notification
from haystack.query import SearchQuerySet
from core import choices as core_choices
from student.models import Student
from employer import enums
from employer.models import ResumeBook, StudentComment, Employer, Industry
from student import enums as student_enums
from core.digg_paginator import DiggPaginator


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

def get_paginator(request):
    current_ordered_results = combine_and_order_results(get_cached_filtering_results(request), get_cached_search_results(request), request.POST['ordering'], request.POST['query'])
    processed_ordered_results = process_results(request.user.recruiter, current_ordered_results)
    current_paginator = DiggPaginator(processed_ordered_results, int(request.POST['results_per_page']), body=5, padding=1, margin=2)
    return current_paginator

def get_is_starred_attributes(recruiter, students):
    starred_attr_dict = {}
    for student in students:
        if student in recruiter.starred_students.all():
            starred_attr_dict[student] = True
        else:
            starred_attr_dict[student] = False
    return starred_attr_dict

def get_comments(recruiter, students):
    comments_dict = {}
    for student in students:
        student_comments = StudentComment.objects.filter(recruiter=recruiter, student=student)
        if student_comments.exists():
            comments_dict[student] = student_comments[0].comment
        else:
            StudentComment.objects.create(recruiter=recruiter, student=student, comment="")
            comments_dict[student] = ""   
    return comments_dict

def process_results(recruiter, students):
    is_in_resume_book_attributes = get_is_in_resumebook_attributes(recruiter, students)
    is_starred_attributes = get_is_starred_attributes(recruiter, students)
    comments = get_comments(recruiter, students)
    return [(student, is_in_resume_book_attributes[student], is_starred_attributes[student], comments[student]) for student in students]

def get_is_in_resumebook_attributes(recruiter, students):
    resume_book_dict = {}
    resume_books = ResumeBook.objects.filter(recruiter = recruiter)
    if not resume_books.exists():
        latest_resume_book = ResumeBook.objects.create(recruiter = recruiter)
    else:
        latest_resume_book = resume_books.order_by('-date_created')[0]
    for student in students:
        if student in latest_resume_book.students.all():
            resume_book_dict[student] = True
        else:
            resume_book_dict[student] = False
    return resume_book_dict
    
def get_cached_filtering_results(request):
    cached_filtering_results = cache.get('filtering_results')
    if cached_filtering_results:
        return cached_filtering_results
    else:
        gpa = None
        if request.POST['gpa'] != "0":
            gpa = request.POST['gpa']
        
        act = None
        if request.POST['act'] != "0":
            act = request.POST['act']
        
        sat_t = None
        if request.POST['sat_t'] != "600":
            sat_t = request.POST['sat_t']

        sat_m = None
        if request.POST['sat_m'] != "200":
            sat_m = request.POST['sat_m']
            
        sat_v = None
        if request.POST['sat_v'] != "200":
            sat_v = request.POST['sat_v']

        sat_w = None
        if request.POST['sat_w'] != "200":
            sat_w = request.POST['sat_w']

        courses = None
        if request.POST['courses']:
            courses = request.POST['courses'].split('~')
        
        school_years = None
        if request.POST['school_years']:
            school_years = request.POST['school_years'].split('~')
            
        graduation_years = None
        if request.POST['graduation_years']:
            graduation_years = request.POST['graduation_years'].split('~')
        
        employment_types = None
        if request.POST['employment_types']:
            employment_types = request.POST['employment_types'].split('~')

        previous_employers = None
        if request.POST['previous_employers']:
            previous_employers = request.POST['previous_employers'].split('~')
        
        industries_of_interest = None
        if request.POST['industries_of_interest']:
            industries_of_interest = request.POST['industries_of_interest'].split('~')
        
        gender=None
        if request.POST['gender']:
            gender = request.POST['gender']

        older_than_18 = None
        if request.POST['older_than_18'] != 'N':
            older_than_18 = request.POST['older_than_18']
        
        ethnicities = None
        if request.POST['ethnicities']:
            ethnicities = request.POST['ethnicities'].split('~')
            
        languages = None
        if request.POST['languages']:
            languages  = request.POST['languages'].split('~')
        
        countries_of_citizenship = None
        if request.POST['countries_of_citizenship']:
            countries_of_citizenship = request.POST['countries_of_citizenship'].split('~')
            
        campus_orgs = None
        if request.POST['campus_orgs']:
            campus_orgs  = request.POST['campus_orgs'].split('~')
                                
        current_filtering_results = filter_students(request.user.recruiter,
                                                    student_list=request.POST['student_list'],
                                                    gpa=gpa,
                                                    courses = courses,
                                                    school_years = school_years,
                                                    graduation_years = graduation_years,
                                                    act=act,
                                                    sat_t=sat_t,
                                                    sat_m=sat_m,
                                                    sat_v=sat_v,
                                                    sat_w=sat_w,
                                                    employment_types=employment_types,
                                                    previous_employers=previous_employers,
                                                    industries_of_interest=industries_of_interest,
                                                    older_than_18 = older_than_18,
                                                    ethnicities=ethnicities,
                                                    languages=languages,
                                                    countries_of_citizenship=countries_of_citizenship,
                                                    gender=gender,
                                                    campus_orgs=campus_orgs)
        
        cache.set('filtering_results', current_filtering_results)
    return current_filtering_results

def get_cached_search_results(request):
    cached_search_results = cache.get('search_results')
    if cached_search_results:
        return cached_search_results
    current_search_results = []
    if request.POST['query'] != "null":
        current_search_results = search_students(request.POST['query'])
    cache.set('search_results', current_search_results)
    return current_search_results
    
def filter_students(recruiter,
                    student_list=None,
                    gpa=None,
                    act=None,
                    sat_t=None, 
                    sat_m=None, 
                    sat_v=None, 
                    sat_w=None, 
                    courses=None,
                    school_years=None,
                    graduation_years=None,
                    employment_types=None,
                    previous_employers=None,
                    industries_of_interest=None,
                    gender=None,
                    older_than_18=None,
                    ethnicities=None,
                    languages=None,
                    countries_of_citizenship=None,
                    campus_orgs=None):
    # All Students
    if student_list == student_enums.GENERAL_STUDENT_LISTS[0][1]:
        students = Student.objects.all()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[1][1]:
        pass
        # all starred students
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[2][1]:
        resume_books = ResumeBook.objects.filter(recruiter = recruiter)
        if not resume_books.exists():
            latest_resume_book = ResumeBook.objects.create(recruiter = recruiter)
        else:
            latest_resume_book = resume_books.order_by('-date_created')[0]
        students = latest_resume_book.students.all()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[3][1]:
        pass
        # latest default filtering parameter matches students
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[4][1]:
        pass
        # all default filtering parameter matches
    
    kwargs = {}
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
    if school_years:
        kwargs['school_year__id__in'] = school_years
    if graduation_years:
        kwargs['graduation_year__id__in'] = graduation_years
    if employment_types:
        kwargs['looking_for__id__in'] = employment_types
    if previous_employers:
        kwargs['previous_employers__id__in'] = previous_employers
    if industries_of_interest:
        kwargs['industries_of_interest__id__in'] = industries_of_interest
    if gender and gender != core_choices.BOTH_GENDERS:
        kwargs['gender'] = gender
    if older_than_18:
        kwargs['older_than_18'] = older_than_18
    if ethnicities:
        kwargs['ethnicity__id__in'] = ethnicities
    if languages:
        kwargs['languages__id__in'] = languages
    if countries_of_citizenship:
        kwargs['countries_of_citizenship__iso__in'] = countries_of_citizenship
    if campus_orgs:
        kwargs['campus_involvement__id__in'] = campus_orgs
    filtering_results = students.filter(**kwargs)

    if courses:
        filtering_results = filtering_results.filter(Q(first_major__id__in=courses) | Q(second_major__id__in=courses))
    
    return filtering_results


def search_students(query):
    search_query_set = SearchQuerySet().models(Student).filter(content=query)
    return [result.object for result in search_query_set]
    

def combine_and_order_results(filtering_results, search_results, ordering, query):
    ordered_results = []
    if search_results:
        if ordering == enums.ORDERING_CHOICES[0][0]:
            for student in search_results:
                if student in filtering_results:
                    ordered_results.append(student)
        else:
            filtering_results.order_by(ordering)
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

def employer_search_helper(request):
    search_results = SearchQuerySet().models(Employer)
    has_events = True if request.GET.get('h', 'false')=='true' else False
    if has_events:
        search_results = search_results.filter(has_events=True)
    industry_id = request.GET.get('i', None)
    if industry_id:
        search_results = search_results.filter(industries=industry_id)
    query = request.GET.get('q', None)
    if query:
        for q in query.split(' '):
            if q.strip() != "":
                search_results = search_results.filter(content_auto=q)
    return map(lambda n: n.object, search_results)
