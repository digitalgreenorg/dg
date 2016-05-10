import datetime
from django.db import models
from django.contrib.auth.models import User

from base_models import QACocoModel, TYPE_CHOICES

from geographies.models import District
from programs.models import Partner
from videos.models import Category, SubCategory, Video

class FullDownloadStats(models.Model):
    user = models.ForeignKey(User, related_name="qacoco_user",)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class ServerLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    user = models.ForeignKey(User, related_name="qacocoserverlog_user", null=True)
    village = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)
    partner = models.IntegerField(null=True)

class QACocoUser(models.Model):
	user = models.ForeignKey(User)
	partner = models.ForeignKey(Partner)
	districts = models.ManyToManyField(District)
	def get_districts(self):
		return self.districts.all()
	
	def __unicode__(self):
		return  u'%s' % (self.user.username)

class QAReviewer(models.Model):
	reviewer_name = models.CharField(max_length=20)

	def __unicode__(self):
		return u'%s' % (self.reviewer_name)

class VideoContentApproval(QACocoModel):
    video = models.ForeignKey(Video)
    qareviewer = models.ForeignKey(QAReviewer)
    suitable_for = models.IntegerField(max_length=1,choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, default=None)
    sub_category = models.ForeignKey(SubCategory)
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        display = "%s" % (self.video)
        return display
