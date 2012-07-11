from dashboard.fields import *
from dashboard.models import TopPractice, SubPractice, PracticeUtility, \
    PracticeType, PracticeSubject, Video
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class PracticeCombination(models.Model):
    id = BigAutoField(primary_key = True)
    top_practice = BigForeignKey(TopPractice)
    sub_practice = BigForeignKey(SubPractice, null=True)
    utility = BigForeignKey(PracticeUtility, null=True)
    type = BigForeignKey(PracticeType, null=True)
    subject = BigForeignKey(PracticeSubject, null=True)
    
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