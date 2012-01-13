from core.decorators import is_student, is_recruiter, is_campus_org
from core.views import handle_500

class UserIntegrity(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            if not request.user.is_staff:
                user = request.user
                if request.META['SERVER_NAME'] != "testserver" and not (is_student(user) or is_recruiter(user) or is_campus_org(user)):
                    return handle_500(request, "#50001 - Your account was not set up correctly.")
                elif is_recruiter(user):
                    employer = user.recruiter.employer
                    if not employer.slug:
                        return handle_500(request, "#50002 - Employer profile is missing a mandatory slug.")
                    elif not employer.main_contact:
                        return handle_500(request, "#50003 - Employer profile is missing the mandatory main contact name.")
                    elif not employer.main_contact_email:
                        return handle_500(request, "#50004 - Employer profile is missing the mandatory main contact email.")
        return None