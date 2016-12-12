from django.contrib.auth.models import User
from django.db import models

# Variables
TYPE_OF_ROLE = (
	(1, 'MRP'),
	(0, 'Animator'),
)

DAY_CHOICES = (
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

VIDEO_TYPE = (
        (1, 'Eligible for Adoption'),
        (2, 'Not Eligible for adoption')
)

STORYBASE = (
        (1, 'Agricultural'),
        (2, 'Institutional'),
        (3, 'Health'),
)

ADOPTION_VERIFICATION = (
    (0, 'Not Checked'),
    (1, 'Approved'),
    (2, 'Rejected'),
)

SCREENING_OBSERVATION = (
    (0, 'Not Observed'),
    (1, 'Observed'),
)

SCREENING_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

VIDEO_REVIEW = (
    (0, 'Not Reviewed'),
    (1, 'Reviewed'),
)

VIDEO_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

VERIFIED_BY = (
    (0,'Digital Green'),
    (1,'Partner'),
    (2,'Third Party'),
)

REVIEW_BY = (
    (0,'Digital Green'),
    (1,'Partner'),
)

NONNEGOTIABLE_OPTION = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
)

TYPE_OF_COCOUSER = (
    (1, 'HNN'),
    (2, 'AGRICULTURE'),
    (3, 'BOTH'),
    )

PARENT_CATEGORY = (
    (1, 'HNN'),
    (2, 'AGRICULTURE'),
    )

ATTENDED_PERSON_CATEGORY = (
    (0,'Pregnant Woman'),
    (1,'Mother of a child up to 6 months'),
    (2,'Mother of a child 6 months to 2 years'),
    (3,'Mother of a child  2 to 5 years'),
    (4,'Adolescent girl (10-19 years)'),
    (5, 'Woman of reproductive age (15-49 years)'),
)


class CocoModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
