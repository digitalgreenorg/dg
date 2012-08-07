from dashboard.fields import *
from dashboard.models import PracticeMain, PracticeSub, PracticeSector, \
    PracticeSubSector, PracticeSubject, Video
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class PracticeCombination(models.Model):
    id = BigAutoField(primary_key = True)
    top_practice = BigForeignKey(PracticeSector) #Didn't rename variable to 'sector' to avoid unnecessary labor. This going to removed anyway.
    sub_practice = BigForeignKey(PracticeSubSector, null=True)
    utility = BigForeignKey(PracticeMain, null=True)
    type = BigForeignKey(PracticeSub, null=True)
    subject = BigForeignKey(PracticeSubject, null=True)
    
    class Meta:
        unique_together = ("top_practice", "sub_practice", "utility", "type", "subject")
    
class VideoPractice(models.Model):
    id = BigAutoField(primary_key = True)
    video = BigForeignKey(Video)
    practice = BigForeignKey(PracticeCombination)
    user = models.ForeignKey(User, null=True)
    review_user = models.ForeignKey(User, null=True, related_name='reviewed_practices')
    review_approved = models.NullBooleanField(null=True)
    
class SkippedVideo(models.Model):
    video = BigForeignKey(Video)
    user = models.ForeignKey(User)