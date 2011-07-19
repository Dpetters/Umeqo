ACTIVE = 1
INACTIVE = 0

QUESTION_STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)

ALL = 0
ANONYMOUS = 1
STUDENT = 2
EMPLOYER = 3

TOPIC_AUDIENCE_CHOICES = (
    (ALL, 'All'),
    (ANONYMOUS, 'Anonymous'),
    (STUDENT, 'Student'),
    (EMPLOYER, 'Employer')
)