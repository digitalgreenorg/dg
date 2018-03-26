from django.contrib.auth.models import User
from django.db import models

# Variables
TYPE_OF_ROLE = (
	(1, 'MRP'),
	(0, 'Animator'),
)

ACTIVITY_CHOICES = (
    ('MKSP', 'MKSP'),
    ('LIVELIHOOD', 'LIVELIHOOD'),
    ('GOTARY', 'GOTARY'),
    ('HNN', 'HNN'),
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
    (4, 'UPAVAN'),
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

ADOPT_PRACTICE_CATEGORY = (
    ("1",'Yes'),
    ("2",'No'),
    ("3",'Not Applicable'),
)

FRONTLINE_WORKER_PRESENT = (
    ("1",'ANM'),
    ("2",'ASHA'),
    ("3",'AWW'),
)

TYPE_OF_VENUE = (

    ('1', 'AWC'),
    ('2', 'school'),
    ('3', 'open space'),
    ('4', 'community hall'),
    ('5', 'other'),
)

TYPE_OF_VIDEO = (

    ('1', 'NSA video'),
    ('2', 'MIYCN video'),
    ('3', 'PLA video'),
    ('4', 'PLA meeting'),
)

TOPICS   = (

    ('1', 'Introduction and understanding social inequities'),
    ('2', 'Understanding underlying causes of under nutrition'),
    ('3', 'Identifying problems that affect nutrition conditions during the 1000-day'),
    ('4', 'Prioritizing problems'),
    ('5', 'Understanding the causes and effects'),
    ('6', 'Understanding barriers and opportunities'),
    ('7', 'Accountability and sharing of Responsibilities'),
    ('8', 'Planning and sharing of responsibilities for Village interface Meeting')
)


class CocoModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
