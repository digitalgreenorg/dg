import datetime
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from qacoco.qa_data_log import delete_log, save_log
from base_models import QACocoModel, TYPE_CHOICES, SCORE_CHOICES, VIDEO_GRADE, APPROVAL, ADOPTED, EQUIPMENT_WORK

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

class QACocoUser(QACocoModel):
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
post_save.connect(save_log, sender=QAReviewer)
pre_delete.connect(delete_log, sender=QAReviewer)

class QAReviewerName(models.Model):
    reviewer_category = models.ForeignKey(QAReviewer)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.name)
post_save.connect(save_log, sender=QAReviewerName)
pre_delete.connect(delete_log, sender=QAReviewerName)

class VideoContentApproval(QACocoModel):
    video = models.ForeignKey(Video)
    qareviewername = models.ForeignKey(QAReviewerName)
    suitable_for = models.IntegerField(validators=[MaxValueValidator(9)],choices=TYPE_CHOICES)
    comment = models.CharField(max_length=200)
    
    def __unicode__(self):
        display = u'%s' % (self.video)
        return display
post_save.connect(save_log, sender=VideoContentApproval)
pre_delete.connect(delete_log, sender=VideoContentApproval)

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
    qareviewername = models.ForeignKey(QAReviewerName)
    remarks = models.CharField(max_length=200)
   
    def __unicode__(self):
        display = "%s" % (self.video)
        return display
post_save.connect(save_log, sender=VideoQualityReview)
pre_delete.connect(delete_log, sender=VideoQualityReview)

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
    qareviewername = models.ForeignKey(QAReviewerName)
    remark = models.CharField(max_length=200)
    pico = models.CharField(max_length=1, choices=EQUIPMENT_WORK)
    speaker = models.CharField(max_length=1, choices=EQUIPMENT_WORK)

    class Meta:
        verbose_name_plural = "Dissemination qualities"
post_save.connect(save_log, sender=DisseminationQuality)
pre_delete.connect(delete_log, sender=DisseminationQuality)

class AdoptionVerification(QACocoModel):   
    block = models.ForeignKey(Block)
    mediator = models.ForeignKey(Animator)
    village = models.ForeignKey(Village)
    group = models.ForeignKey(PersonGroup)
    person = models.ForeignKey(Person)
    verification_date = models.DateField()
    video = models.ForeignKey(Video)
    qareviewername = models.ForeignKey(QAReviewerName)
    adopted = models.IntegerField(choices=ADOPTED, null=True)
post_save.connect(save_log, sender=AdoptionVerification)
pre_delete.connect(delete_log, sender=AdoptionVerification)
