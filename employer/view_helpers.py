import logging

from django.core.cache import cache
from django.http import Http404

from core.view_helpers import search
from haystack.query import SearchQuerySet, SQ
from student.models import Student
from employer import enums
from employer.models import ResumeBook, Employer, EmployerStudentComment
from student import enums as student_enums
from events.models import Event
from core.digg_paginator import DiggPaginator

# Get an instance of a logger
logger = logging.getLogger("django.request")

def get_cached_paginator(request):
    cached_paginator = cache.get('paginator')
    if cached_paginator:
        print "using cached paginator);"
        logger.warning('using the cached paginator!')
        return cache.get("filtering"), cached_paginator
    else:
        print "not using cached paginator"
        logger.warning('NOT using the cached paginator!')
        filtering, cached_ordered_results = get_cached_ordered_results(request)
        paginator = DiggPaginator(cached_ordered_results, int(request.GET['results_per_page']), body=5, padding=1, margin=2)
        cache.set("paginator", paginator)
        return filtering, paginator

def get_cached_ordered_results(request):
    cached_ordered_results = cache.get("ordered_results")
    if cached_ordered_results:
        print "using cached_ordered_results"
        logger.warning('using the cached_ordered_results!')
        return cache.get("filtering"), cached_ordered_results
    else:
        print "NOT using cached_ordered_results"
        logger.warning('NOT using the cached_ordered_results!')
        filtering, cached_results = get_cached_results(request)
        ordered_results = [search_result.object for search_result in order_results(cached_results, request).load_all()]
        cache.set("ordered_results", ordered_results)
        return filtering, ordered_results

def get_cached_results(request):
    results = cache.get('results')
    if results:
        print "using cached results"
        logger.warning('using the cached results!')
        return cache.get("filtering"), results
    else:
        print "NOT using cached results"
        logger.warning('NOT using the cached results!')
        student_list = request.GET['student_list']
        student_list_id = request.GET['student_list_id']
        recruiter = request.user.recruiter

        if student_list == student_enums.GENERAL_STUDENT_LISTS[0][1] and recruiter.employer.subscribed_annually():
            students = SearchQuerySet().models(Student)
        else:
            if student_list == student_enums.GENERAL_STUDENT_LISTS[0][1]:
                students = get_students_in_resume_book(recruiter)
            elif student_list == student_enums.GENERAL_STUDENT_LISTS[1][1]:
                students = recruiter.employer.starred_students
            elif student_list == student_enums.GENERAL_STUDENT_LISTS[2][1]:
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
                        students = Student.objects.filter(rsvp__in=e.rsvp_set.filter(attending=True), profile_created=True).visible()
                    elif parts[-1] == "Attendees":
                        students = Student.objects.filter(attendee__in=e.attendee_set.all(), profile_created=True).visible()
                    elif parts[-1] == "Drop" and parts[-2] == "Resume":
                        students = Student.objects.filter(droppedresume__in=e.droppedresume_set.all(), profile_created=True).visible()
                else:
                    students = ResumeBook.objects.get(id = student_list_id).students.visible()
            students = SearchQuerySet().models(Student).filter(obj_id__in = [student.id for student in students])
                
        am_filtering = False

        if request.GET.has_key('gpa'):
            am_filtering = True
            students = students.filter(gpa__gte = request.GET['gpa'])
        
        if request.GET.has_key('act'):
            am_filtering = True
            students = students.filter(act__gte = request.GET['act'])
        
        if request.GET.has_key('sat_t'):
            am_filtering = True            
            students = students.filter(sat_t__gte = request.GET['sat_t'])

        if request.GET.has_key('sat_m'):
            am_filtering = True            
            students = students.filter(sat_m__gte = request.GET['sat_m'])
            
        if request.GET.has_key('sat_v'):
            am_filtering = True            
            students = students.filter(sat_v__gte = request.GET['sat_v'])

        if request.GET.has_key('sat_w'):
            am_filtering = True            
            students = students.filter(sat_w__gte = request.GET['sat_w'])
        
        if request.GET.has_key('school_years'):
            am_filtering = True
            students = students.filter(school_year__in = request.GET['school_years'].split('~'))
            
        if request.GET.has_key('graduation_years'):
            am_filtering = True            
            students = students.filter(graduation_year__in = request.GET['graduation_years'].split('~'))
        
        if request.GET.has_key('employment_types'):
            am_filtering = True            
            students = students.filter(looking_for__in = request.GET['employment_types'].split('~'))

        if request.GET.has_key('previous_employers'):
            am_filtering = True            
            students = students.filter(previous_employers__in = request.GET['previous_employers'].split('~'))
        
        if request.GET.has_key('industries_of_interest'):
            am_filtering = True            
            students = students.filter(industries_of_interest__in = request.GET['industries_of_interest'].split('~'))

        if request.GET.has_key('languages'):
            am_filtering = True            
            students = students.filter(languages__in = request.GET['languages'].split('~'))
        
        if request.GET.has_key('campus_orgs'):
            am_filtering = True            
            students = students.filter(campus_orgs__in = request.GET['campus_orgs'].split('~'))

        if request.GET.has_key('countries_of_citizenship'):
            am_filtering = True            
            students = students.filter(countries_of_citizenship__in =  request.GET['countries_of_citizenship'].split('~'))
            
        if request.GET['older_than_21'] != 'N':
            am_filtering = True
            students = students.filter(older_than_21 = True)

        if request.GET.has_key('courses'):
            am_filtering = True
            courses = request.GET['courses'].split('~')
            students = students.filter(SQ(first_major__in = courses)|SQ(second_major__in = courses))
        
        if request.GET.has_key('query'):
            students = search(students, request.GET['query'])
        
        cache.set("results", students)
        return am_filtering, students
    
def get_is_starred_attributes(recruiter, students):
    starred_attr_dict = {}
    starred_students = recruiter.employer.starred_students.all()
    for student in students:
        if student in starred_students:
            starred_attr_dict[student] = True
        else:
            starred_attr_dict[student] = False
    return starred_attr_dict

def get_comments(recruiter, students):
    comments_dict = {}
    employer_comments = EmployerStudentComment.objects.filter(employer=recruiter.employer)
    for student in students:
        try:
            comments_dict[student] = employer_comments.get(student=student).comment
        except EmployerStudentComment.DoesNotExist:
            EmployerStudentComment.objects.create(employer=recruiter.employer, student=student, comment="")
            comments_dict[student] = ""   
    return comments_dict

def get_num_of_events_attended_dict(recruiter, students):
    num_of_events_attended_dict = {}
    recruiter_events = recruiter.user.event_set.all()
    for student in students:
        num_of_events_attended_dict[student] = len(recruiter_events.filter(attendee__student=student))
    return num_of_events_attended_dict

def process_results(recruiter, page):
    is_in_resume_book_attributes = get_is_in_resumebook_attributes(recruiter, page.object_list)
    is_starred_attributes = get_is_starred_attributes(recruiter, page.object_list)
    comments = get_comments(recruiter, page.object_list)
    num_of_events_attended_dict = get_num_of_events_attended_dict(recruiter, page.object_list)
    return [(student, is_in_resume_book_attributes[student], is_starred_attributes[student], comments[student], num_of_events_attended_dict[student]) for student in page.object_list]

def get_is_in_resumebook_attributes(recruiter, students):
    resume_book_dict = {}
    try:
        resume_book = ResumeBook.objects.get(recruiter=recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter=recruiter)
    resume_book_students = resume_book.students.all()
    for student in students:
        if student in resume_book_students:
            resume_book_dict[student] = True
        else:
            resume_book_dict[student] = False
    return resume_book_dict

                
def get_students_in_resume_book(recruiter):
    try:
        resume_book = ResumeBook.objects.get(recruiter = recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter = recruiter)
    return resume_book.students.visible()

def order_results(results, request):
    if request.GET['ordering'] != enums.RELEVANCY:
        results = results.order_by(request.GET['ordering'])
    else:
        if not request.GET.has_key("query"):
            results = results.order_by("-last_updated")
    return results

def employer_search_helper(request):
    search_results = SearchQuerySet().models(Employer).filter(visible=True)

    if request.GET.get('subscribed', False)=='true':
        search_results = search_results.filter(subscribers=request.user.id)
    
    # filter by whether the employer has an upcoming event or not
    if request.GET.get('has_public_events_deadlines', False)=="true":
        search_results = search_results.filter(has_public_events=True)
        
    # filter by industry
    industry_id = request.GET.get('i', None)
    if industry_id:
        search_results = search_results.filter(industries=industry_id)
    
    # search
    if request.GET.get('q'):
        search_results = search(search_results, request.GET.get('q'))
    # Extract the object.
    employers = map(lambda n: n.object, search_results)
    # Sort the employers.
    return sorted(employers, key=lambda n: n.name)