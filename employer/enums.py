RESULTS_PER_PAGE_CHOICES = (
(5, 5),
(10, 10),
(20, 20),
(30, 30),
(50, 50),
(100, 100),
)

ORDERING_CHOICES = (
("relevancy", "Relevancy"),
("gpa", "Lowest GPA First"),
("-gpa", "Highest GPA First"),
)

DOWNLOAD = "d"
EMAIL = "e"
RESUME_BOOK_DELIVERY_CHOICES = (
(DOWNLOAD, "Download"),
(EMAIL, "Email")
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