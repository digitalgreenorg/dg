from django.contrib.auth.models import User
from django.db import models


# Variables
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
        (1, 'Demonstration'),
        (2, 'Success story/ Testimonial'),
        (3, 'Activity Introduction'),
        (4, 'Discussion'),
        (5, 'General Awareness'),
)

STORYBASE = (
        (1, 'Agricultural'),
        (2, 'Institutional'),
        (3, 'Health'),
)

ACTORS = (
        ('I', 'Individual'),
        ('F', 'Family'),
        ('G', 'Group'),
)

SUITABLE_FOR = (
        (1, 'Dissemination'),
        (2, 'Video Production Training'),
        (3, 'Dissemination Training'),
        (4, 'Nothing'),
        (5, 'Pending for Approval'),
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

class CocoModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
