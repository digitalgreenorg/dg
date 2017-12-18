# django imports
from django.db import models
from django.db.models.signals import pre_delete 
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator
# app imports
from coco.data_log import delete_log
from coco.data_log import save_log
from coco.base_models import CocoModel
from coco.base_models import STORYBASE
from coco.base_models import VIDEO_TYPE
from coco.base_models import VIDEO_GRADE
from coco.base_models import VIDEO_REVIEW
from coco.base_models import REVIEW_BY
from coco.base_models import PARENT_CATEGORY
from geographies.models import Village
from programs.models import Partner
from people.models import Animator
from people.models import Person
from training.log.training_log import enter_to_log
from django.template.defaultfilters import truncatechars


class PracticeSector(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubSector(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeTopic(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubtopic(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubject(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class Practice(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    practice_name = models.CharField(null=True, blank=True, max_length=200)
    practice_sector = models.ForeignKey(PracticeSector, default=1)
    practice_subsector = models.ForeignKey(PracticeSubSector, null=True, blank=True)
    practice_topic = models.ForeignKey(PracticeTopic, null=True, blank=True)
    practice_subtopic = models.ForeignKey(PracticeSubtopic, null=True, blank=True)
    practice_subject = models.ForeignKey(PracticeSubject, null=True, blank=True)

    class Meta:
        verbose_name = "Practice"
        unique_together = ("practice_sector", "practice_subsector", "practice_topic", "practice_subtopic", "practice_subject")

    def __unicode__(self):
        practice_sector = '' if self.practice_sector is None else self.practice_sector.name
        practice_subject = '' if self.practice_subject is None else self.practice_subject.name
        practice_subsector = '' if self.practice_subsector is None else self.practice_subsector.name
        practice_topic = '' if self.practice_topic is None else self.practice_topic.name
        practice_subtopic = '' if self.practice_subtopic is None else self.practice_subtopic.name
        return "%s, %s, %s, %s, %s" % (practice_sector, practice_subject, practice_subsector, practice_topic, practice_subtopic)


class ParentCategory(CocoModel):
    id = models.AutoField(primary_key=True)
    parent_category_name = models.CharField(max_length=100, unique='True')

    class Meta:
        verbose_name_plural = "ParentCategory"

    def __unicode__(self):
        return self.parent_category_name


class Category(CocoModel):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique='True')
    parent_category = models.ForeignKey(ParentCategory, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.category_name == "Agriculture":
            self.parent_category_id=2
        if self.category_name in ['Child Health and Nutrition', 'Nutrition-sensitive approaches', "Women's Health and Nutrition"]:
            self.parent_category_id=1
            return super(Category, self).save(*args, **kwargs)

    def get_village(self):
        return None

    def get_partner(self):
        return None

    class Meta:
        verbose_name_plural = "categories"

    def __unicode__(self):
        return self.category_name


class DirectBeneficiaries(models.Model):
    """
    Describes the direct beneficiaries of the video
    """
    direct_beneficiaries_category = models.CharField(max_length=80, null=True)
    category = models.ManyToManyField(Category, blank=True)

    def __unicode__(self):
        return self.direct_beneficiaries_category

class SubCategory(CocoModel):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category)
    subcategory_name = models.CharField(max_length = 100)

    def get_village(self):
        return None

    def get_partner(self):
        return None

    class Meta:
        verbose_name_plural = "sub categories"

    def __unicode__(self):
        return self.subcategory_name

class VideoPractice(CocoModel):
    id = models.AutoField(primary_key=True)
    subcategory = models.ForeignKey(SubCategory)
    videopractice_name = models.CharField(max_length = 100)

    def get_village(self):
        return None

    def get_partner(self):
        return None

    def __unicode__(self):
        return self.videopractice_name

class Language(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    language_name = models.CharField(max_length=100, unique='True')

    def get_village(self):
        return None

    def get_partner(self):
        return None

    def __unicode__(self):
        return self.language_name
post_save.connect(save_log, sender=Language)
pre_delete.connect(delete_log, sender=Language)
post_save.connect(enter_to_log, sender=Language)
pre_delete.connect(enter_to_log,sender=Language)


class Video(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    title = models.CharField(max_length=200)
    video_type = models.IntegerField(choices=VIDEO_TYPE,validators=[MaxValueValidator(2)])
    duration = models.TimeField(null=True, blank=True)
    language = models.ForeignKey(Language)
    benefit = models.TextField(blank=True)
    production_date = models.DateField()
    village = models.ForeignKey(Village)
    production_team = models.ManyToManyField(Animator)
    category = models.ForeignKey(Category, null=True, blank=True)
    direct_beneficiaries = models.ManyToManyField(DirectBeneficiaries, blank=True)
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True)
    videopractice = models.ManyToManyField(VideoPractice, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    related_practice = models.ForeignKey(Practice, blank=True, null=True)
    youtubeid = models.CharField(max_length=20, blank=True)
    partner = models.ForeignKey(Partner)
    review_status = models.IntegerField(choices=VIDEO_REVIEW,default=0, validators=[MaxValueValidator(1)])
    video_grade = models.CharField(max_length=1,choices=VIDEO_GRADE,null=True,blank=True)
    reviewer = models.IntegerField(verbose_name="Organisation", choices=REVIEW_BY, null=True, blank=True, validators=[MaxValueValidator(1)])
    reviewed_by = models.CharField(max_length=80, null=True, blank=True)
    self_reported_behaviour1 = models.CharField(max_length=500, null=True, blank=True)
    self_reported_behaviour2 = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        unique_together = ("title", "production_date", "language", "village")

    def __unicode__(self):
        return  u'%s (%s)' % (self.title, self.village)

    def location(self):
        return u'%s (%s) (%s) (%s)' % (self.village.village_name, self.village.block.block_name, self.village.block.district.district_name, self.village.block.district.state.state_name)
post_save.connect(save_log, sender=Video)
pre_delete.connect(delete_log, sender=Video)

class NonNegotiable(CocoModel):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video)
    non_negotiable = models.CharField(max_length=500)
    physically_verifiable = models.BooleanField(db_index=True, default=False)

    def __unicode__(self):
        return  u'%s' % self.non_negotiable
post_save.connect(save_log, sender=NonNegotiable)
pre_delete.connect(delete_log, sender=NonNegotiable)


class JSLPS_Video(CocoModel):
    id = models.AutoField(primary_key=True)
    vc = models.CharField(max_length=100)
    video = models.ForeignKey(Video, null=True, blank=True)


class APVideo(CocoModel):
    video = models.ForeignKey(Video, null=True, blank=True)
    video_short_name = models.CharField(max_length=40)
    video_short_regionalname = models.CharField(max_length=40)
    bluefrog_practice = models.CharField(max_length=40)

    
    @property
    def short_video_title(self):
        return truncatechars(self.video.title, 50)


    def __unicode__(self):
        return """%s:%s:%s""" % (str(self.id), self.video.title, self.video_short_name)


