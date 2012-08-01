from dashboard.fields import *
from dashboard.models import Practices, PracticeTopic, PracticeSubtopic, PracticeSector, \
    PracticeSubSector, PracticeSubject, Video
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class VideoPractice(models.Model):
    id = BigAutoField(primary_key = True)
    video = BigForeignKey(Video)
    practice = BigForeignKey(Practices)
    user = models.ForeignKey(User, null=True)
    review_user = models.ForeignKey(User, null=True, related_name='reviewed_practices')
    review_approved = models.NullBooleanField(null=True)
    
class SkippedVideo(models.Model):
    video = BigForeignKey(Video)
    user = models.ForeignKey(User)