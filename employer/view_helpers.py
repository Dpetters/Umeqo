from django.db.models import Q
from django.core.cache import cache
from django.http import Http404

from haystack.query import SearchQuerySet
from student.models import Student
from employer import enums
from employer.models import ResumeBook, Employer, EmployerStudentComment
from student import enums as student_enums
from events.models import Event
from core.digg_paginator import DiggPaginator
        
def get_paginator(request):
    filtering, current_ordered_results = combine_and_order_results(get_cached_filtering_results(request), get_cached_search_results(request), request.POST['ordering'], request.POST['query'])
    processed_ordered_results = process_results(request.user.recruiter, current_ordered_results)
    return filtering, DiggPaginator(processed_ordered_results, int(request.POST['results_per_page']), body=5, padding=1, margin=2)

def get_is_starred_attributes(recruiter, students):
    starred_attr_dict = {}
    for student in students:
        if student in recruiter.employer.starred_students.all():
            starred_attr_dict[student] = True
        else:
            starred_attr_dict[student] = False
    return starred_attr_dict

def get_comments(recruiter, students):
    comments_dict = {}
    for student in students:
        try:
            comments_dict[student] = EmployerStudentComment.objects.get(employer=recruiter.employer, student=student).comment
        except EmployerStudentComment.DoesNotExist:
            EmployerStudentComment.objects.create(employer=recruiter.employer, student=student, comment="")
            comments_dict[student] = ""   
    return comments_dict

def get_num_of_events_attended_dict(recruiter, students):
    num_of_events_attended_dict = {}
    for student in students:
        num_of_events_attended_dict[student] = len(recruiter.user.event_set.filter(attendee__student=student))
    return num_of_events_attended_dict

def process_results(recruiter, students):
    is_in_resume_book_attributes = get_is_in_resumebook_attributes(recruiter, students)
    is_starred_attributes = get_is_starred_attributes(recruiter, students)
    comments = get_comments(recruiter, students)
    num_of_events_attended_dict = get_num_of_events_attended_dict(recruiter, students)
    return [(student, is_in_resume_book_attributes[student], is_starred_attributes[student], comments[student], num_of_events_attended_dict[student]) for student in students]

def get_is_in_resumebook_attributes(recruiter, students):
    resume_book_dict = {}
    try:
        resume_book = ResumeBook.objects.get(recruiter=recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter=recruiter)
    for student in students:
        if student in resume_book.students.all():
            resume_book_dict[student] = True
        else:
            resume_book_dict[student] = False
    return resume_book_dict
    
def get_cached_filtering_results(request):
    cached_filtering_results = cache.get('filtering_results')
    if cached_filtering_results:
        return True, cached_filtering_results
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
                                
        filtering, current_filtering_results = filter_students(request.user.recruiter,
                                                    student_list=request.POST['student_list'],
                                                    student_list_id=request.POST['student_list_id'],
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
    return filtering, current_filtering_results


def get_cached_search_results(request):
    cached_search_results = cache.get('search_results')
    if cached_search_results:
        return True, cached_search_results
    current_search_results = []
    filtering = False
    if request.POST['query'] != "null":
        filtering = True
        current_search_results = search_students(request.POST['query'])
    cache.set('search_results', current_search_results)
    return filtering, current_search_results

def get_students_in_resume_book(recruiter):
    try:
        resume_book = ResumeBook.objects.get(recruiter = recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = recruiter)
    return resume_book.students.visible()
        
def filter_students(recruiter,
                    student_list=None,
                    student_list_id=None,
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
        if recruiter.employer.subscribed_annually():
            students = Student.objects.visible()
        else:
            students = get_students_in_resume_book(recruiter)
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[1][1]: # Starred Students
        students = recruiter.employer.starred_students.visible()
    elif student_list == student_enums.GENERAL_STUDENT_LISTS[2][1]: # Students In Current Resume Book
        try:
            resume_book = ResumeBook.objects.get(recruiter = recruiter, delivered=False)
        except ResumeBook.DoesNotExist:
            resume_book = ResumeBook.objects.create(recruiter = recruiter)
        students = resume_book.students.visible()
    else:
        parts = student_list.split(" ")
        if parts[-1] == "RSVPs" or parts[-1] == "Attendees" or parts[-1] == "Drop" and parts[-2] == "Resume":
            try:
                e = Event.objects.get(id = student_list_id)
            except:
                raise Http404
            if parts[-1] == "RSVPs":
                students = Student.objects.filter(rsvp__in=e.rsvp_set.filter(attending=True), profile_created=True)
            elif parts[-1] == "Attendees":
                students = Student.objects.filter(attendee__in=e.attendee_set.all(), profile_created=True)
            elif parts[-1] == "Drop" and parts[-2] == "Resume":
                students = Student.objects.filter(droppedresume__in=e.droppedresume_set.all(), profile_created=True)
        else:
            students = ResumeBook.objects.get(id = student_list_id).students.visible()
    filtering = False
    kwargs = {}
    if gpa:
        filtering = True
        kwargs['gpa__gte'] = gpa
    if act:
        filtering = True
        kwargs['act__gte'] = act
    if sat_t:
        filtering = True
        kwargs['sat_t__gte'] = sat_t
    if sat_m:
        filtering = True
        kwargs['sat_m__gte'] = sat_m
    if sat_v:
        filtering = True
        kwargs['sat_v__gte'] = sat_v
    if sat_w:
        filtering = True
        kwargs['sat_w__gte'] = sat_w
    if school_years:
        filtering = True
        kwargs['school_year__id__in'] = school_years
    if graduation_years:
        filtering = True
        kwargs['graduation_year__id__in'] = graduation_years
    if employment_types:
        filtering = True
        kwargs['looking_for__id__in'] = employment_types
    if previous_employers:
        filtering = True
        kwargs['previous_employers__id__in'] = previous_employers
    if industries_of_interest:
        filtering = True
        kwargs['industries_of_interest__id__in'] = industries_of_interest
    if older_than_21:
        filtering = True
        kwargs['older_than_21'] = older_than_21
    if languages:
        filtering = True
        kwargs['languages__id__in'] = languages
    if countries_of_citizenship:
        filtering = True
        kwargs['countries_of_citizenship__iso__in'] = countries_of_citizenship
    if campus_orgs:
        filtering = True
        kwargs['campus_involvement__id__in'] = campus_orgs
    filtering_results = students.filter(**kwargs)

    if courses:
        filtering = True
        filtering_results = filtering_results.filter(Q(first_major__id__in=courses) | Q(second_major__id__in=courses))
    return filtering, filtering_results.distinct()


def search_students(query):
    search_query_set = SearchQuerySet().models(Student).filter(content=query)
    return [result.object for result in search_query_set]


def combine_and_order_results(filtering_results, search_results, ordering, query):
    ordered_results = []
    filtering = filtering_results[0] or search_results[0]
    
    search_results_students = search_results[1]
    filtering_results_students = filtering_results[1]
    if search_results_students:
        # FIXME(dpetters): should be using the enum, not array indices?
        if ordering == enums.ORDERING_CHOICES[0][0]:
            for student in search_results_students:
                if student in filtering_results_students:
                    ordered_results.append(student)
        else:
            for student in filtering_results_students.order_by(ordering):
                if student in search_results_students:
                    ordered_results.append(student)
        return filtering, ordered_results
    else:
        if query == "null":
            if ordering == enums.ORDERING_CHOICES[0][0]:
                return filtering, filtering_results_students.order_by('-last_updated')
            else:
                return filtering, filtering_results_students.order_by(ordering)
        return filtering, []

def employer_search_helper(request):
    search_results = SearchQuerySet().models(Employer).filter(visible=True)

    if request.GET.get('subscribed', False)=='true':
        search_results = search_results.filter(subscribers=request.user.id)

    if request.GET.get('has_public_events', False)=="true":
        search_results = search_results.filter(has_public_events=True)
        
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
