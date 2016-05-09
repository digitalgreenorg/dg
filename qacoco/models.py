import datetime
from django.db import models
from django.contrib.auth.models import User

from base_models import QACocoModel, TYPE_CHOICES

from geographies.models import District
from programs.models import Partner
from videos.models import Category, SubCategory, Video

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
    reviewer = models.ForeignKey(QAReviewer)
    suitable_for = models.IntegerField(max_length=1,choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, default=None)
    sub_category = models.ForeignKey(SubCategory)
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        display = "%s" % (self.video)
        return display
