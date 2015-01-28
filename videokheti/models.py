import datetime

from django.contrib.auth.models import User
from django.db import models
from videos.models import Video as coco_video


class Crop(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    hindi_text = models.CharField(max_length=1000, blank=True, null=True)

class TimeYear(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    hindi_text = models.CharField(max_length=1000, blank=True, null=True)


class ActionType(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    time_year = models.ForeignKey(TimeYear)
    hindi_text = models.CharField(max_length=1000, blank=True, null=True)


class Method(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    hindi_text = models.CharField(max_length=1000, blank=True, null=True)


class Video(models.Model):
    coco_video = models.ForeignKey(coco_video)
    website_id = models.CharField(max_length=20)
    crop = models.ForeignKey(Crop)
    time_year = models.ForeignKey(TimeYear)
    action_type = models.ForeignKey(ActionType, blank=True, null=True)
    method = models.ForeignKey(Method, blank=True, null=True)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    hindi_text = models.CharField(max_length=1000, blank=True, null=True)


class VideoComment(models.Model):
    date = models.DateField(default=lambda: datetime.datetime.utcnow().date())
    text = models.TextField()
    video = models.ForeignKey(Video)
    user = models.ForeignKey(User, null=True, blank=True)
    imageURL = models.URLField(max_length=400, null=True, blank=True)
    personName = models.CharField(max_length=300, null=True, blank=True)
