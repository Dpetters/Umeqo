"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
YES = 'Y'
NO = 'N'

BOTH_GENDERS = 'B'
MALE = 'M'
FEMALE = 'F'

SELECT_YES_NO_CHOICES = (
('', '--'),
(YES, 'Yes'),
(NO, 'No'),
)

GENDER_CHOICES = (
('', '--'),
(MALE, 'Male'),
(FEMALE, 'Female'),
)

FILTERING_GENDER_CHOICES = (
(BOTH_GENDERS, 'Male and Female'),
(MALE, 'Male'),
(FEMALE, 'Female'),
)

NO_YES_CHOICES = (
(NO, 'No'),
(YES, 'Yes'),
)
