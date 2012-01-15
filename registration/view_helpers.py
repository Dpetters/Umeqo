import re

from django.core.urlresolvers import reverse

from employer.models import Employer
from registration.backend import RegistrationBackend
from student.models import Student

def modify_redirect(request, redirect_to=None):
    if not redirect_to or ' ' in redirect_to or '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
        if hasattr(request.user, 'employer'):
            redirect_to = reverse('home')
        elif hasattr(request.user, "student"):
            redirect_to = reverse('home')
    return redirect_to

def register_student(request, **args):
    new_user = RegistrationBackend().register(request, **args)
    if args.has_key("first_name") and args.has_key("last_name"):
        student = Student(user=new_user, first_name = args["first_name"], last_name = args["last_name"])
    else:
        student = Student(user=new_user)
    umeqo = Employer.objects.get(name="Umeqo")
    student.save()
    if args.has_key("course"):
        student.first_major=args["course"]
    student.subscriptions.add(umeqo)
    student.save()
    return student