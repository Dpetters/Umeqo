from core.search import search
from haystack.query import SearchQuerySet
from employer import enums
from employer.models import ResumeBook, Employer, EmployerStudentComment
from events.models import Attendee

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
    return dict((x.student, x.comment) for x in EmployerStudentComment.objects.filter(employer=recruiter.employer, student__in =students))


def get_num_of_events_attended_dict(recruiter, students):
    attendees = dict((x.student, 1) for x in Attendee.objects.filter(event__in = recruiter.user.event_set.all(), student__in = students))
    num_of_events_attended_dict = {}
    for k, v in attendees.iteritems():
        if num_of_events_attended_dict.has_key(k):
            num_of_events_attended_dict[k] += 1
        else:
            num_of_events_attended_dict[k] = 0
    return num_of_events_attended_dict


def process_results(recruiter, page):
    is_in_resume_book_attributes = get_is_in_resumebook_attributes(recruiter, page.object_list)
    is_starred_attributes = get_is_starred_attributes(recruiter, page.object_list)
    comments = get_comments(recruiter, page.object_list)
    num_of_events_attended_dict = get_num_of_events_attended_dict(recruiter, page.object_list)
    return [(student, is_in_resume_book_attributes.get(student, False), is_starred_attributes.get(student, False), comments.get(student, ""), num_of_events_attended_dict.get(student, 0)) for student in page.object_list]


def get_is_in_resumebook_attributes(recruiter, students):
    resume_book_dict = {}
    try:
        resume_book = ResumeBook.objects.get(recruiter=recruiter, delivered=False)
    except ResumeBook.DoesNotExist:
        resume_book = ResumeBook.objects.create(recruiter=recruiter)
    resume_book_students = resume_book.students.visible()
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