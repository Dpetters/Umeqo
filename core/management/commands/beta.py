import ldap
import random
import string

from pprint import pprint as pp
from optparse import make_option

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.conf import settings

from registration.models import InterestedPerson
from student.models import StudentInvite

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
                person.final = True
                person.save()
                continue
            try:
                con = ldap.open('ldap.mit.edu')
                con.simple_bind_s("", "")
                dn = "dc=mit,dc=edu"
                username = person.email.split("@")[0]
                r = con.search_s(dn, ldap.SCOPE_SUBTREE, 'uid='+username, [])
                if r:
                    if r[0][1]['eduPersonPrimaryAffiliation'][0] == "student":
                        students.append(r[0][1])
                        if options['statistics']:
                            major = r[0][1]['ou'][0]
                            if student_majors.has_key(major):
                                student_majors[major] += 1
                            else:
                                student_majors[major] = 1
                        if options['update']:
                            if not person.final and not person.emailed:
                                # Some people have middle names so I can't just
                                # unpack the values, but instead take first & last
                                fname = r[0][1]['cn'][0].split(" ")[0]
                                lname = r[0][1]['cn'][0].split(" ")[-1]
                                person.first_name = fname
                                person.last_name = lname
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
        if options["email"]:
            for person in InterestedPerson.objects.all():
                if person.auto_email:
                    invite_code = ''.join(random.choice(string.ascii_uppercase + \
                                string.ascii_lowercase + string.digits) for x in range(12))
                    StudentInvite.objects.create(id = invite_code)
                    recipients = [person.email]
                    subject = "Umeqo Beta Invitation" 
                    body = render_to_string('student_beta_invitation_email_body.txt', \
                                            {'first_name':person.student.first_name, \
                                            'last_name':person.student.last_name, \
                                            'email':person.email })
                    message = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
                    #Do NOT uncomment!
                    ####################
                    ###message.send()###
                    ####################
                    # Do NOT uncomment!
                    person.emailed = True
                    person.save()