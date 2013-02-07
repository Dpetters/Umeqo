import re

from django.template import Context
from django.template.loader import render_to_string
from django.conf import settings as s
from django.core.urlresolvers import reverse

from core.email import get_basic_email_context, send_email
from core.models import Course, DomainName
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
    new_user.userattributes.has_agreed_to_terms()
    
    domain = new_user.email.split("@")[1]
    
    if not DomainName.objects.filter(domain=domain).exists():
        #make new domain name
        DomainName.objects.create(domain=domain)

	#send email
	#gets email of team@umeqo.com
        recipients = [mail_tuple[1] for mail_tuple in s.MANAGERS]

        context = Context({'domain':domain})
        context.update(get_basic_email_context())

        txt_email_body = render_to_string('new_domain_email_body.txt', context)

        subject = ''.join(render_to_string('email_admin_subject.txt', {
                'message': "New Domain: %s" % domain
            }, context).splitlines())

        send_email(subject, txt_email_body, recipients)
        
	

    if new_user.first_name and new_user.last_name:
        student = Student(user=new_user, first_name = new_user.first_name, last_name = new_user.last_name)
    else:
        student = Student(user=new_user)
    umeqo = Employer.objects.get(name="Umeqo")
    student.save()
    if args.has_key("course"):
        try:
            course = Course.objects.get(id=args["course"])
        except:
            Course.DoesNotExist
        else:
            student.first_major=course
            
    student.subscriptions.add(umeqo)
    student.save()
    return student
