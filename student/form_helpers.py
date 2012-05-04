from __future__ import division
from __future__ import absolute_import

import ldap

from core.models import Course
from student import enums as student_enums
from employer.models import Recruiter

def is_not_mit_student(ldap_response):
    return not ldap_response or (ldap_response[0] != None and ldap_response[0][1]['eduPersonPrimaryAffiliation'][0] != "student")
    
def get_student_ldap_info(email):
    con = ldap.open('ldap.mit.edu')
    con.simple_bind_s("", "")
    dn = "dc=mit,dc=edu"
    uid = email.split("@")[0]
    return con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])

def get_student_data_from_ldap(email):
    res = get_student_ldap_info(email)
    if is_not_mit_student(res):
        return "", "", None
    fname = res[0][1]['cn'][0].split(" ")[0]
    lname = res[0][1]['cn'][0].split(" ")[-1]
    course_id = None
    try:
        course_id = Course.objects.get(ou = res[0][1]['ou'][0]).id
    except Exception, e:
        pass
    return fname, lname, course_id
                
def student_lists_as_choices(has_at_least_premium, recruiter_id):
    student_list_types = []
    recruiter = Recruiter.objects.get(id=recruiter_id)
    e = recruiter.employer
    for student_list_type in student_enums.STUDENT_LIST_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        if student_list_type[0] == student_enums.GENERAL:
            for student_list in student_enums.GENERAL_STUDENT_LISTS:
                if student_list[0] == student_enums.UNLOCKED_STUDENTS:
                    if not has_at_least_premium: 
                        student_lists.append([0, student_list[1]])
                else:
                    student_lists.append([0, student_list[1]])
        elif student_list_type[0] == student_enums.EVENT:
            events = e.events_attending.all()
            for index, event in enumerate(events):
                student_lists.append([event.id, event.name.replace("\"", "\'") + " RSVPs"])
                student_lists.append([event.id, event.name.replace("\"", "\'") + " Attendees"])
                if event.is_drop:
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " Resume Drop"])
        elif student_list_type[0] == student_enums.RESUME_BOOK_HISTORY:
            rbs = recruiter.resumebook_set.filter(delivered=True)
            for rb in rbs:
                if len(rb.students.visible())> 0:
                    student_lists.append([rb.id, rb.name])
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    return student_list_types
