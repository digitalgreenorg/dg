import datetime

from django.db import models
from django.contrib.auth.models import User

from base_models import CocoModel
from geographies.models import Village
from programs.models import Partner


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

    def get_villages(self):
        return self.villages.all()
    
    def __unicode__(self):
        return  u'%s' % (self.user.username)
