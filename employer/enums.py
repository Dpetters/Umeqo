"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""


RESULTS_PER_PAGE_CHOICES = (
(1,1),
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