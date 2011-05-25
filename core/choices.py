"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
SELECT_YES_NO_CHOICES = (
('', 'select'),
(True, 'Yes'),
(False, 'No'),
)

GENDER_CHOICES = (
('', 'select'),
('M', 'Male'),
('F', 'Female'),
)

BOTH_GENDERS = 0
MALE = 1
FEMALE = 2

FILTERING_GENDER_CHOICES = (
(BOTH_GENDERS, 'Male and Female'),
(MALE, 'Male'),
(FEMALE, 'Female'),
)

NO_YES_CHOICES = (
(False, 'No'),
(True, 'Yes'),
)
