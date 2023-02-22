from django.contrib.auth.models import User
from django.db import models

SCORE_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
)

VIDEO_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

APPROVAL = (
    ('0', 'No'),
    ('1', 'Yes'),
)

ADOPTED = (
    ('0', 'No'),
    ('1', 'Yes'),
)

EQUIPMENT_WORK = (
    ('0', 'Not Working'),
    ('1', 'Working'),
)


class QACocoModel(models.Model):
    user_created = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created", editable=False, null=True, blank=True)
    time_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_related_modified", editable=False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
