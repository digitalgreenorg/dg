from dashboard.fields import *
from videos.models import Practices, PracticeTopic, PracticeSubtopic, PracticeSector, \
    PracticeSubSector, PracticeSubject, Video
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class VideoPractice(models.Model):
    id = BigAutoField(primary_key = True)
    video = BigForeignKey(Video)
    practice = BigForeignKey(Practice)
    user = models.ForeignKey(User, null=True)
    review_user = models.ForeignKey(User, null=True, related_name='reviewed_practices')
    review_approved = models.NullBooleanField(null=True)
    def __unicode__(self):
        return self.video.title
    
    class Meta:
        unique_together = ("video", "review_user")
    def save(self, *args, **kwargs):
        if VideoPractice.objects.filter(video=self.video,review_user=self.review_user).count()>0:
            return
        else:
            super(VideoPractice, self).save(*args, **kwargs) 

class SkippedVideo(models.Model):
    video = BigForeignKey(Video)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.user.username + " "+self.video.title
