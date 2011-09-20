ALL = 0
ANONYMOUS = 1
AUTHENTICATED = 2
STUDENT = 3
EMPLOYER = 4
CAMPUS_ORG = 5
CAMPUS_ORGS_AND_EMPLOYERS = 6

TOPIC_AUDIENCE_CHOICES = (
    (ALL, 'All'),
    (ANONYMOUS, 'Anonymous'),
    (AUTHENTICATED, 'Authenticated'),
    (STUDENT, 'Students'),
    (EMPLOYER, 'Employers'),
    (CAMPUS_ORG, 'Campus Orgs'),
    (CAMPUS_ORGS_AND_EMPLOYERS, 'Campus Orgs & Employers')
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