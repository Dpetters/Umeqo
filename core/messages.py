from django.conf import settings as s

search_filter_find = "Umeqo presents you with not only a student's resume, but also info applicable to your firm, such as event attendance. Potential candidates can be added to custom resume books that can be emailed and/or downloaded."

# Employer Students
no_students_selected = "No students selected."
wait_until_resume_book_is_ready = "Please wait until the resume book is ready."


#Account Settinggs
password_changed = 'Password changed successfully.'

profile_saved = 'Your profile has been saved.'

# Campus Org Profile Form
campus_org_name_required = "Organization name is required."
campus_org_type_required = "Organization type is required."

#Event Page
drop_resume_tooltip = "Logged-in students can click this button to drop off their resume."
rsvp_yes_tooltip = "Logged-in students can click this button to RSVP."

#Employer Profile 
employer_name_required = "You must specify an employer name"

# Employer Profile Preview
subscribe_tooltip = "Logged-in students can click this button to subscribe to your employer for new event and deadline notifications."

#Student Profile Form
first_name_required = 'Enter your first name.'
last_name_required= 'Enter your last name.'
school_year_required = "Choose your school year."
graduation_year_required = 'Choose your graduation year.'
first_major_required = 'Choose your major.'
gpa_required = 'Enter your GPA.'
gpa_range = 'Your GPA should be between 0 and 5.'
resume_required = "Please select a PDF version of your resume."
invalid_url = 'Please enter a valid url.'
first_second_majors_diff = "Second major must be different from first."
student_profile_preview_checkbox_tooltip = "Employers use these checkboxes to \
perform actions over multiple students at once."

max_languages_exceeded = "You can select at most %s languages." % s.SP_MAX_LANGUAGES
one_language_difficulty = "You can only select one language difficulty."
max_previous_employers_exceeded = "You can select at most %s employers." % s.SP_MAX_PREVIOUS_EMPLOYERS
max_industries_of_interest_exceeded = "You can select at most %s industries." % s.SP_MAX_INDUSTRIES_OF_INTEREST
max_countries_of_citizenship_exceeded = "You can select at most %s countries." % s.SP_MAX_COUNTRIES_OF_CITIZENSHIP
max_campus_involvement_exceeded = "You can select at most %s campus organizations." % s.SP_MAX_CAMPUS_INVOLVEMENT

star_toggle_tooltip = "If you stand out, a recruiter can star you! You will \
appear as such to all the other recruiters at that company."

resume_book_current_toggle_tooltip = "Recruiters can toggle you in and out of \
the custom resume book they're creating."

comment_text = "Recruiters write comments about you for later referral!"
event_attendance_tooltip = "A company's recruiters only see this icon on your \
profile if you attended at least one of their events. Upon hover they see a \
summary of the events which you attended."

invite_to_event_tooltip = "Recruiters can invite you to both public and \
private events."

view_resume_tooltip = "Apart from creating resume books, recruiters can also \
view and download your resume individually."

campus_org_already_exists = "This campus organization already exists."
language_already_exists = "This language already exists."

# Employer Profile Form
slug_required = "You need to pick a slug!"
industries_required = "You need to pick 1-5 industries."
description_required = "A description is required."
main_contact_required = "You need to specify a main contact."
main_contact_email_required = "An email is required for the main contact."
invalid_phone = "Doesn't look like a valid phone #."
max_industries_exceeded = "You can select at most %s industries." % s.EP_MAX_INDUSTRIES

# Resume
resume_problem = "There was a problem with your resume. Try again."
empty_resume = "We could not extract any keywords out of your resume."

# Student Event Invitations
already_invited = "Student has already been invited."

# Login Form
incorrect_username_password_combo = "The username and password combo that you \
entered is invalid. Please note that both fields are case-sensitive."

staff_member_login_not_allowed = "Staff users cannot login. They can only \
access the admin pages."

account_suspended = "This account has been suspended. Feel free to contact us by clicking the link in the footer."

enable_cookies = "Your browser doesn't seem to have cookies enabled. \
Cookies are required to login."


# Contact Form
thank_you_for_contacting_us = "We have received your message. Thank you for \
contacting us!"

contact_us_message_spam = "Our system thinks your message is spam. If you \
think this is a mistake, email us instead."


# Password Reset Form
passwords_dont_match = "The two passwords don't match."
email_not_registered = "This email is not registered."

# Password Change Form
incorrect_old_password = "Your password was incorrect."

# New event form
start_datetime_required = "Start date and time are required."
end_datetime_required = "End date and time are required."

# Student Registration
email_required = "What's your email?"
invalid_email = "Doesn't look like a valid email."
must_be_mit_email = "Must be an MIT email."
email_already_registered = "This email is already registered."
password_required = "You need a password!"
must_be_mit_student = "You must be a student to sign up."
ldap_server_error = "Can't contact LDAP server. Try again in a few min."
invalid_invite_code = "Sorry, but this invite code is invalid."
invite_code_required = "You need an invite code!"
invite_code_already_used = "This code has already been used."