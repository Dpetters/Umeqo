from __future__ import division
from __future__ import absolute_import

import ldap
import inspect
import types

from core.models import Course
from student import enums as student_enums
from employer.models import Recruiter

memoized_metaclasses_map = {}

def skip_redundant(iterable, skipset=None):
    "Redundant items are repeated items or items in the original skipset."
    if skipset is None: skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item

def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses: # determines the metaclasses to be skipped
        skipset.update(inspect.getmro(meta)[1:])
    return tuple(skip_redundant(metaclasses, skipset))

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    # make tuple of needed metaclasses in specified priority order
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)

    # return existing confict-solving meta, if any
    if needed_metas in memoized_metaclasses_map:
        return memoized_metaclasses_map[needed_metas]
    # nope: compute, memoize and return needed conflict-solving meta
    elif not needed_metas:         # wee, a trivial case, happy us
        meta = type
    elif len(needed_metas) == 1: # another trivial case
        meta = needed_metas[0]
    # check for recursion, can happen i.e. for Zope ExtensionClasses
    elif needed_metas == bases: 
        raise TypeError("Incompatible root metatypes", needed_metas)
    else: # gotta work ...
        metaname = '_' + ''.join([m.__name__ for m in needed_metas])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta

def classmaker(left_metas=(), right_metas=()):
    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)
    return make_class

def get_student_ldap_info(email):
    con = ldap.open('ldap.mit.edu')
    con.simple_bind_s("", "")
    dn = "dc=mit,dc=edu"
    uid = email.split("@")[0]
    return con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+uid, [])

def get_student_data_from_ldap(email):
    res = get_student_ldap_info(email)
    fname = res[0][1]['cn'][0].split(" ")[0]
    lname = res[0][1]['cn'][0].split(" ")[-1]
    course_id = None
    try:
        course_id = Course.objects.get(ou = res[0][1]['ou'][0]).id
    except Exception, e:
        pass
    return fname, lname, course_id
                
def student_lists_as_choices(recruiter_id):
    student_list_types = []
    recruiter = Recruiter.objects.get(id=recruiter_id)
    e = recruiter.employer
    for student_list_type in student_enums.STUDENT_LIST_TYPE_CHOICES:
        new_student_list_type = []
        student_lists = []
        if student_list_type[0] == student_enums.GENERAL:
            for student_list in student_enums.GENERAL_STUDENT_LISTS:
                if not e.subscribed_annually() and ( student_list[1] == student_enums.GENERAL_STUDENT_LISTS[0][1] or student_list[1] == student_enums.GENERAL_STUDENT_LISTS[1][1]):
                    student_lists.append([0, student_list[1], "disabled=\"disabled\""])
                elif not e.subscribed_annually() and student_list[1] == student_enums.GENERAL_STUDENT_LISTS[2][1]:
                    student_lists.append([0, student_list[1], "selected=\"selected\""])
                else:
                    student_lists.append([0, student_list[1]])
        elif student_list_type[0] == student_enums.EVENT:
            events = e.event_set.all()
            for index, event in enumerate(events):
                if index == 0 and not e.subscribed_annually():
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " RSVPs", "selected=\"selected\""])
                else:
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " RSVPs"])
                student_lists.append([event.id, event.name.replace("\"", "\'") + " Attendees"])
                if event.is_drop:
                    student_lists.append([event.id, event.name.replace("\"", "\'") + " Resume Drop"])
        elif student_list_type[0] == student_enums.RESUME_BOOK_HISTORY:
            rbs = recruiter.resumebook_set.filter(delivered=True)
            for rb in rbs:
                if not e.subscribed_annually():
                    student_lists.append([rb.id, rb.name, "disabled=\"disabled\""])
                else:
                    student_lists.append([rb.id, rb.name])
        new_student_list_type = [student_list_type[1], student_lists]
        student_list_types.append(new_student_list_type)
    return student_list_types
