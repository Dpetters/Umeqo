TINY = "t"
SMALL = "s"
MEDIUM = "m"
LARGE = "l"

EMPLOYER_SIZE_CHOICES = (
    ("", "select # of employees"),
    (TINY, "< 10"),
    (SMALL, "10-100"),
    (MEDIUM, "101-500"),
    (LARGE, "501+")
)


COUPLE = 'c'
FEW = 'f'
MANY = 'm'
HIRE_NUM_CHOICES = (
    ("", "choose # of students"),
    (COUPLE, "1-3"),
    (FEW, "4-12"),
    (MANY, "13+")
)

MONTHLY = 1
QUARTERLY = 3
ANNUAL = 12

SUBSCRIPTION_RECURRENCE_CHOICES = (
(MONTHLY, "Monthly"),
(QUARTERLY, "Quarterly"),
(ANNUAL, "Annual"),
)