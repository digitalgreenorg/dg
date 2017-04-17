import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from base_models import CocoModel
from data_log import upload_entries
from geographies.models import Village
from programs.models import Partner
from videos.models import Video


class FullDownloadStats(models.Model):
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class ServerLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    user = models.ForeignKey(User, related_name="serverlog_user", null=True)
    village = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)
    partner = models.IntegerField(null=True)


class CocoUser(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.IntegerField(editable=False, null=True)
    user = models.OneToOneField(User, related_name="coco_user")
    partner = models.ForeignKey(Partner)
    villages = models.ManyToManyField(Village)
    videos = models.ManyToManyField(Video)

    def get_villages(self):
        return self.villages.all()

    def get_videos(self):
        return self.videos.all()

    def __unicode__(self):
        return  u'%s' % (self.user.username)


def validate_file_extension(value):
    if not value.name.endswith('.json'):
        raise ValidationError(u'Please Upload the File downloaded from CoCo')


class UploadEntries(CocoModel):
    upload_file = models.FileField(upload_to='coco_entries/', validators=[validate_file_extension])
    user = models.ForeignKey(User, editable=False, null=True)
post_save.connect(upload_entries, sender=UploadEntries)
