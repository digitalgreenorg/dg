from django.db import models
from django.db.models.signals import pre_delete, post_save

from coco.data_log import delete_log, save_log
from coco.base_models import CocoModel
from geographies.models import Village
from programs.models import Partner
from people.models import Animator, Person, PersonGroup
from videos.models import Video

class Screening(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True)
    village = models.ForeignKey(Village)
    animator = models.ForeignKey(Animator)
    farmer_groups_targeted = models.ManyToManyField(PersonGroup)
    videoes_screened = models.ManyToManyField(Video)
    farmers_attendance = models.ManyToManyField(Person, through='PersonMeetingAttendance', blank='False', null='False')
    partner = models.ForeignKey(Partner)

    class Meta:
        unique_together = ("date", "start_time", "end_time","animator","village")

    def __unicode__(self):
        return u'%s %s' % (self.date, self.village)

post_save.connect(save_log, sender=Screening)
pre_delete.connect(delete_log, sender=Screening)


class PersonMeetingAttendance(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    screening = models.ForeignKey(Screening)
    person = models.ForeignKey(Person)
    interested = models.BooleanField(db_index=True)
    expressed_question = models.CharField(max_length=500, blank=True)
    expressed_adoption_video = models.ForeignKey(Video, related_name='expressed_adoption_video', null=True, blank=True)

    def __unicode__(self):
        return  u'%s' % (self.id)

class PersonAdoptPractice(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    person = models.ForeignKey(Person)
    video = models.ForeignKey(Video)
    date_of_adoption = models.DateField()
    partner = models.ForeignKey(Partner)

    def __unicode__(self):
        return "%s (%s) (%s) (%s)" % (self.person.person_name, self.person.father_name, self.person.village.village_name, self.video.title)

    def get_village(self):
        return self.person.village.id

    def get_partner(self):
        return self.partner.id

    class Meta:
        unique_together = ("person", "video", "date_of_adoption")
post_save.connect(save_log, sender=PersonAdoptPractice)
pre_delete.connect(delete_log, sender=PersonAdoptPractice)