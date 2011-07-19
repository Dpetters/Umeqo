from django.db.models import Q
from django.core.cache import cache

from notification import models as notification
from haystack.query import SearchQuerySet
from student.models import Student
from employer import enums
from employer.models import ResumeBook, StudentComment, Employer
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
    return DiggPaginator(processed_ordered_results, int(request.POST['results_per_page']), body=5, padding=1, margin=2)

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
        try:
            comments_dict[student] = StudentComment.objects.get(recruiter=recruiter, student=student).comment
        except StudentComment.DoesNotExist:
            StudentComment.objects.create(recruiter=recruiter, student=student, comment="")
            comments_dict[student] = ""   
    return comments_dict

def get_num_of_events_attended_dict(recruiter, students):
    num_of_events_attended_dict = {}
    for student in students:
        num_of_events_attended_dict[student] = len(recruiter.event_set.filter(attendee__student=student))
    return num_of_events_attended_dict

def process_results(recruiter, students):
    is_in_resume_book_attributes = get_is_in_resumebook_attributes(recruiter, students)
    is_starred_attributes = get_is_starred_attributes(recruiter, students)
    comments = get_comments(recruiter, students)
    num_of_events_attended_dict = get_num_of_events_attended_dict(recruiter, students)
    return [(student, is_in_resume_book_attributes[student], is_starred_attributes[student], comments[student], num_of_events_attended_dict[student]) for student in students]

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
        
        older_than_21 = None
        if request.POST['older_than_21'] != 'N':
            older_than_21 = request.POST['older_than_21']

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
                                                    older_than_21 = older_than_21,
                                                    languages=languages,
                                                    countries_of_citizenship=countries_of_citizenship,
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
                    older_than_21=None,
                    languages=None,
                    countries_of_citizenship=None,
                    campus_orgs=None):

    if student_list == student_enums.GENERAL_STUDENT_LISTS[0][1]: # All Students
        students = Student.objects.visible()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[1][1]: # Starred Students
        students = recruiter.starred_students.visible()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[2][1]: # Students In Current Resume Book
        resume_books = ResumeBook.objects.filter(recruiter = recruiter)
        if not resume_books.exists():
            latest_resume_book = ResumeBook.objects.create(recruiter = recruiter)
        else:
            latest_resume_book = resume_books.order_by('-date_created')[0]
        students = latest_resume_book.students.visible()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[3][1]: # New Default Filtering Matches 
        pass
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[4][1]: # All Default Filtering Matches
        pass
    
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
    if older_than_21:
        kwargs['older_than_21'] = older_than_21
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
        # FIXME(dpetters): should be using the enum, not array indices?
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
    in_subscriptions = True if request.GET.get('s', 'false')=='true' else False
    if in_subscriptions:
        search_results = search_results.filter(subscribers=request.user.id)
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
    # Extract the object.
    employers = map(lambda n: n.object, search_results)
    # Sort the employers.
    return sorted(employers, key=lambda n: n.name)
