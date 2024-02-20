import datetime
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from qacoco.qa_data_log import delete_log, save_log
from base_models import QACocoModel, SCORE_CHOICES, VIDEO_GRADE, APPROVAL, ADOPTED, EQUIPMENT_WORK

from geographies.models import District, Block, Village
from programs.models import Partner
from videos.models import Category, SubCategory, Video, NonNegotiable
from people.models import Animator, Person, PersonGroup


class FullDownloadStats(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="qacoco_user",)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class ServerLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    user = models.ForeignKey(
        User, related_name="qacocoserverlog_user", null=True)
    block = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)
    partner = models.IntegerField(null=True)


class QACocoUser(QACocoModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User)
    partner = models.ForeignKey(Partner)
    blocks = models.ManyToManyField(Block)
    videos = models.ManyToManyField(Video)

    def get_videos(self):
        return self.videos.all()

    def get_blocks(self):
        return self.blocks.all()

    def __unicode__(self):
        return u'%s' % (self.user.username)


class QAReviewerCategory(QACocoModel):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.category_name)


post_save.connect(save_log, sender=QAReviewerCategory)
pre_delete.connect(delete_log, sender=QAReviewerCategory)


class QAReviewerName(QACocoModel):
    id = models.AutoField(primary_key=True)
    reviewer_category = models.ForeignKey(QAReviewerCategory)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.name)


post_save.connect(save_log, sender=QAReviewerName)
pre_delete.connect(delete_log, sender=QAReviewerName)


class VideoQualityReview(QACocoModel):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video)
    date = models.DateField(null=True)
    storystructure = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    framing = models.CharField(max_length=1, choices=SCORE_CHOICES, blank=True)
    continuity = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    camera_angles = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    camera_movement = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    light = models.CharField(max_length=1, choices=SCORE_CHOICES, blank=True)
    audio_sound = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    # Newly added fields below
    editing = models.CharField(max_length=1, choices=SCORE_CHOICES, blank=True)
    intro_and_importance = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    facilitation = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    non_negotiable_pts = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    story_board = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    ease_of_understanding = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    gender_sensitivity = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    csa_sensitivity = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    # End of newly added fields

    # Abandoned fields below
    interview = models.CharField(
        max_length=1, choices=SCORE_CHOICES, null=True, blank=True, default=None)
    technical = models.CharField(
        max_length=1, choices=SCORE_CHOICES, null=True, blank=True, default=None)
    style_guide = models.CharField(
        max_length=1, choices=SCORE_CHOICES, null=True, blank=True, default=None)
    # End of abandoned fields
    total_score = models.IntegerField()
    video_grade = models.CharField(max_length=1, choices=VIDEO_GRADE)
    #approval = models.IntegerField(choices=APPROVAL)
    approval = models.CharField(max_length=1, choices=APPROVAL)
    qareviewername = models.ForeignKey(QAReviewerName)
    remarks = models.CharField(max_length=200)

    def __unicode__(self):
        display = "%s" % (self.video)
        return display


post_save.connect(save_log, sender=VideoQualityReview)
pre_delete.connect(delete_log, sender=VideoQualityReview)


class DisseminationQuality(QACocoModel):
    id = models.AutoField(primary_key=True)
    block = models.ForeignKey(Block)
    village = models.ForeignKey(Village)
    mediator = models.ForeignKey(Animator)
    video = models.ForeignKey(Video, null=True, blank=True)
    videoes_screened = models.ManyToManyField(Video, related_name="dissemination_observations")
    date = models.DateField()
    equipments_setup_handling = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    # Field abandoned as it has been liquefied into 3 fields
    context_setting = models.CharField(
        max_length=1, choices=SCORE_CHOICES, null=True, default=None, blank=True)
    # End
    # Newly introduced fields
    group = models.ForeignKey(PersonGroup, null=True, default=None)
    maintained_ideal_darkness = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    maintained_ideal_screen_size = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    maintained_ideal_av_quality = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    established_logical_conn = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    # End of newly introduced fields
    introduce_topic = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    paused_video = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    encouraged_adoption = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    summarized_video = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    subject_knowledge = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    filled_dissemination = models.CharField(
        max_length=1, choices=SCORE_CHOICES, blank=True)
    total_score = models.IntegerField()
    video_grade = models.CharField(
        max_length=1, choices=VIDEO_GRADE, null=True, blank=True)
    qareviewername = models.ForeignKey(QAReviewerName)
    remark = models.CharField(max_length=200)
    pico = models.CharField(max_length=1, choices=EQUIPMENT_WORK)
    speaker = models.CharField(max_length=1, choices=EQUIPMENT_WORK)
    remote = models.CharField(max_length=1, null=True, choices=EQUIPMENT_WORK)

    class Meta:
        verbose_name_plural = "Dissemination qualities"


post_save.connect(save_log, sender=DisseminationQuality)
pre_delete.connect(delete_log, sender=DisseminationQuality)


class AdoptionVerification(QACocoModel):
    id = models.AutoField(primary_key=True)
    block = models.ForeignKey(Block)
    mediator = models.ForeignKey(Animator)
    village = models.ForeignKey(Village)
    group = models.ForeignKey(PersonGroup)
    person = models.ForeignKey(Person)
    verification_date = models.DateField()
    video = models.ForeignKey(Video)
    qareviewername = models.ForeignKey(QAReviewerName)
    adopt_nonnegotiable = models.ManyToManyField(
        NonNegotiable, through='AdoptionNonNegotiableVerfication', blank=True)


post_save.connect(save_log, sender=AdoptionVerification)
pre_delete.connect(delete_log, sender=AdoptionVerification)


class AdoptionNonNegotiableVerfication(QACocoModel):
    id = models.AutoField(primary_key=True)
    adoptionverification = models.ForeignKey(AdoptionVerification)
    nonnegotiable = models.ForeignKey(NonNegotiable)
    adopted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % (self.id)
