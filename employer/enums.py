RESULTS_PER_PAGE_CHOICES = (
(10, 10),
(30, 30),
(50, 50),
)

RELEVANCY = "relevancy"
GPA_A = "gpa"
GPA_D = "-gpa"

ORDERING_CHOICES = (
("relevancy", "Relevancy"),
("gpa", "Lowest GPA First"),
("-gpa", "Highest GPA First"),
("first_name", "Alphabetical"),
)

ADDED = "a"
REMOVED = "r"
STUDENT_RESUME_BOOK_ACTIONS = (
(ADDED, "Added"),
(REMOVED, "Removed"),
)

STARRED = "s"
UNSTARRED = "u"
STUDENT_STAR_ACTIONS = (
(STARRED, "Starred"),
(UNSTARRED, "Unstarred"),
)
