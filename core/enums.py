ALL = 0
ANONYMOUS = 1
AUTHENTICATED = 2
STUDENT = 3
EMPLOYER = 4
CAMPUS_ORG = 5
CAMPUS_ORGS_AND_EMPLOYERS = 6
ANONYMOUS_AND_STUDENTS = 7
ANONYMOUS_AND_EMPLOYERS = 8
ANONYMOUS_AND_CAMPUS_ORGS = 9

TOPIC_AUDIENCE_CHOICES = (
    (ALL, 'All'),
    (ANONYMOUS, 'Anonymous'),
    (AUTHENTICATED, 'Authenticated'),
    (STUDENT, 'Students'),
    (EMPLOYER, 'Employers'),
    (CAMPUS_ORG, 'Campus Orgs'),
    (CAMPUS_ORGS_AND_EMPLOYERS, 'Campus Orgs & Employers'),
    (ANONYMOUS_AND_STUDENTS, 'Anonymous & Students'),
    (ANONYMOUS_AND_EMPLOYERS, 'Anonymous & Employers'),
    (ANONYMOUS_AND_CAMPUS_ORGS, 'Anonymous & Campus Orgs'),
)

DOWNLOAD = "d"
EMAIL = "e"
DELIVERY_CHOICES = (
(DOWNLOAD, "Download"),
(EMAIL, "Email")
)

CSV = "c"
XLS = "x"
TEXT = "t"
EXPORT_CHOICES = (
(CSV, "CSV"),
(TEXT, "Text")
)