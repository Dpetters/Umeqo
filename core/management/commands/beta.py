import ldap
import random
import string

from pprint import pprint as pp
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.validators import validate_email

from registration.models import InterestedPerson

INVITE_CODE_LENGTH = 12

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--verbose', action='store_true', dest='verbose', default=False, help='Print out names and emails addresses.'),
        make_option('--update', action='store_true', dest='update', default=False, help='Mark each person (except those marked as final) as someone who will get emailed or not.'),
        make_option('--email', action='store_true', dest='email', default=False, help='Generate invite codes and send beta invitations out'),
        make_option('--statistics', action='store_true', dest='statistics', default=False, help='Generate student statistics')
        )
    
    def handle(self, *args, **options):
        students = []
        not_students = []
        student_majors = {}
        for person in InterestedPerson.objects.all():
            try:
                validate_email(person.email)
            except Exception, e:
                print "Error: %s" % e
                return
            
            try:
                con = ldap.open('ldap.mit.edu')
                con.simple_bind_s("", "")
                dn = "dc=mit,dc=edu"
                username = person.email.split("@")[0]
                result = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+username, [])
                if result:
                    if result[0][1]['eduPersonPrimaryAffiliation'][0] == "student":
                        students.append(result[0][1])
                        if options['statistics']:
                            major = result[0][1]['ou'][0]
                            if student_majors.has_key(major):
                                student_majors[major] += 1
                            else:
                                student_majors[major] = 1
                        if options['update']:
                            if not person.final and not person.emailed:
                                person.auto_email = True
                                person.save()
                    else:
                        not_students.append(person)
                        if options['update']:
                            if not person.final and not person.emailed:
                                person.auto_email = False
                                person.save()
                else:
                    not_students.append(person)
                    if options['update']:
                        if not person.final and not person.emailed:
                            person.auto_email = False
                            person.save()
            except Exception, e:
                print "Error: %s" % e
        print "TOTAL BETA SIGN-UPS: %d" % (len(students) + len(not_students))
        print "\n%d STUDENTS" % (len(students))
        if options["statistics"]:
            print "\nSTUDENT MAJOR STATS:"
            pp(student_majors)
        if options["verbose"]:
            for person in students:
                print "%s (%s)" % (person['cn'][0], person['mail'][0])
        print "\n%d NON-STUDENTS" % (len(not_students))
        if options["verbose"]:
            for person in not_students:
                print "%s %s (%s)" % (person.first_name, person.last_name, person.email)
"""
    for person in InterestedPerson.objects.all():
        StudentInvite.objects.create(id=''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(12)))
        recipients = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
        subject = "%s %s (%s) Account Deactivation" % (request.user.student.first_name, request.user.student.last_name, request.user.username) 
        body = render_to_string('student_account_deactivate_email_body.txt', \
                                {'first_name':request.user.student.first_name, \
                                'last_name':request.user.student.last_name, \
                                'email':request.user.email, \
                                'suggestion':form.cleaned_data['suggestion']})
        message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
        message.send()
"""