import datetime

def get_resume_book_filename(instance, filename):
    return "employer/ResumeBook/" + instance.recruiter + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"

def get_logo_filename(instance, filename):
    return "employer/Employer/" + instance.last_name + "_" + instance.first_name + "_" + str(instance.user) + "_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".pdf"