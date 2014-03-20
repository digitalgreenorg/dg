from django.db import models
from django.db.models.signals import pre_delete, post_save

from dashboard.data_log import delete_log, save_log
from dashboard.base_models import ACTORS, CocoModel, STORYBASE, SUITABLE_FOR, VIDEO_TYPE
from geographies.models import Village
from programmes.models import Partner
from people.models import Animator, Person


class PracticeSector(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubSector(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeTopic(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubtopic(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class PracticeSubject(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class Practice(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    practice_name = models.CharField(null=True, max_length=200)
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


class Language(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    name = models.CharField(max_length=100, unique='True')

    def __unicode__(self):
        return self.name
post_save.connect(save_log, sender=Language)
pre_delete.connect(delete_log, sender=Language)


class Video(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    title = models.CharField(max_length=200)
    video_type = models.IntegerField(max_length=1, choices=VIDEO_TYPE)
    duration = models.TimeField(null=True, blank=True)
    language = models.ForeignKey(Language)
    summary = models.TextField(blank=True)
    picture_quality = models.CharField(max_length=200, blank=True)
    audio_quality = models.CharField(max_length=200, blank=True)
    editing_quality = models.CharField(max_length=200, blank=True)
    edit_start_date = models.DateField(null=True, blank=True)
    edit_finish_date = models.DateField(null=True, blank=True)
    thematic_quality = models.CharField(max_length=200, blank=True)
    video_production_start_date = models.DateField()
    video_production_end_date = models.DateField()
    storybase = models.IntegerField(max_length=1, choices=STORYBASE, null=True, blank=True)
    storyboard_filename = models.FileField(upload_to='storyboard', blank=True)
    raw_filename = models.FileField(upload_to='rawfile', blank=True)
    movie_maker_project_filename = models.FileField(upload_to='movie_maker_project_file', blank=True)
    final_edited_filename = models.FileField(upload_to='final_edited_file', blank=True)
    village = models.ForeignKey(Village)
    facilitator = models.ForeignKey(Animator, related_name='facilitator')
    cameraoperator = models.ForeignKey(Animator, related_name='cameraoperator')
    approval_date = models.DateField(null=True, blank=True)
    supplementary_video_produced = models.ForeignKey('self', null=True, blank=True)
    video_suitable_for = models.IntegerField(choices=SUITABLE_FOR)
    remarks = models.TextField(blank=True)
    related_practice = models.ForeignKey(Practice, blank=True, null=True)
    farmers_shown = models.ManyToManyField(Person)
    actors = models.CharField(max_length=1, choices=ACTORS)
    last_modified = models.DateTimeField(auto_now=True)
    youtubeid = models.CharField(max_length=20, blank=True)
    viewers = models.PositiveIntegerField(default=0, editable=False)
    partner = models.ForeignKey(Partner)

    class Meta:
        unique_together = ("title", "video_production_start_date", "video_production_end_date", "village")

    def __unicode__(self):
        return  u'%s (%s)' % (self.title, self.village)
post_save.connect(save_log, sender=Video)
pre_delete.connect(delete_log, sender=Video)