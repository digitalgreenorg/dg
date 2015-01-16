from django.db import models
from videos.models import Video


class Crop(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)


class TimeYear(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)


class ActionType(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
    time_year = models.ForeignKey(TimeYear)


class Method(models.Model):
    name = models.CharField(max_length=45)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)


class Video(models.Model):
    coco_video = models.ForeignKey(Video)
    website_id = models.CharField(max_length=20)
    crop = models.ForeignKey(Crop)
    time_year = models.ForeignKey(TimeYear)
    action_type = models.ForeignKey(ActionType, blank=True, null=True)
    method = models.ForeignKey(Method, blank=True, null=True)
    image_file = models.CharField(max_length=100)
    sound_file = models.CharField(max_length=100)
