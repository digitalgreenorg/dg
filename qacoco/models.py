import datetime
from django.db import models
from django.contrib.auth.models import User

from base_models import QACocoModel, TYPE_CHOICES, SCORE_CHOICES, VIDEO_GRADE, APPROVAL

from geographies.models import District,Block,Village
from programs.models import Partner
from videos.models import Category, SubCategory, Video, NonNegotiable
from people.models import Animator, Person, PersonGroup

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
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        display = u'%s' % (self.video)
        return display

class VideoQualityReview(QACocoModel):
    video = models.ForeignKey(Video)
    youtubeid = models.CharField(max_length=100)
    storystructure = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    framing = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    camera_angles = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    camera_movement = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    light = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    audio_sound = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    continuity = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    interview = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    technical = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    style_guide = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    total_score = models.IntegerField()
    video_grade = models.CharField(max_length=1,choices=VIDEO_GRADE)
    approval = models.IntegerField(choices=APPROVAL)
    qareviewer = models.ForeignKey(QAReviewer)
    remarks = models.CharField(max_length=200)
   
    def __unicode__(self):
        display = "%s" % (self.video)
        return display

class DisseminationQuality(QACocoModel):
    block = models.ForeignKey(Block)
    village = models.ForeignKey(Village)
    mediator = models.ForeignKey(Animator)
    video = models.ForeignKey(Video)
    date = models.DateField()
    equipments_setup_handling = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    context_setting = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    facilitation = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    subject_knowledge = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    documentation = models.IntegerField(choices=SCORE_CHOICES,null=True,blank=True)
    total_score = models.IntegerField()
    video_grade = models.CharField(max_length=1,choices=VIDEO_GRADE,null=True,blank=True)
    qareviewer = models.ForeignKey(QAReviewer)
    remark = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Dissemination qualities"

class AdoptionVerification(QACocoModel):   
    block = models.ForeignKey(Block)
    mediator = models.ForeignKey(Animator)
    village = models.ForeignKey(Village)
    group = models.ForeignKey(PersonGroup)
    person = models.ForeignKey(Person)
    verification_date = models.DateField()
    video = models.ForeignKey(Video)
    qareviewer = models.ForeignKey(QAReviewer)