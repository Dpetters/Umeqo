ALL = 0
ANONYMOUS = 1
AUTHENTICATED = 2
STUDENT = 3
EMPLOYER = 4
CAMPUS_ORG = 5

TOPIC_AUDIENCE_CHOICES = (
    (ALL, 'All'),
    (ANONYMOUS, 'Anonymous'),
    (AUTHENTICATED, 'Authenticated'),
    (STUDENT, 'Student'),
    (EMPLOYER, 'Employer'),
    (CAMPUS_ORG, 'Campus Org')
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