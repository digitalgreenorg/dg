import json, datetime
from django.db import models
from django.db.models.signals import pre_delete, post_save

from coco.data_log import delete_log, save_log
from coco.base_models import CocoModel
from geographies.models import Village
from programs.models import Partner
from people.models import Animator, Person, PersonGroup
from videos.models import Video
from coco.base_models import ADOPTION_VERIFICATION

class VRPpayment(models.Manager):

    "Custom manager filters standard query set with given args."
    def __init__(self, partner_id, block_id, start_period, end_period):
        super(VRPpayment, self).__init__()
        self.start_yyyy = start_period[-4:]
        self.start_mm = start_period[:2]
        self.start_dd = 01
        self.end_yyyy = end_period[-4:]
        self.end_mm = end_period[:2]
        self.end_dd = 01
        self.partner_id = partner_id
        self.block_id = block_id
        self.Screening_all_object = Screening.objects.filter(village__block_id = self.block_id, partner_id=self.partner_id, date__gte=datetime.date(int(self.start_yyyy), int(self.start_mm), self.start_dd), date__lte=datetime.date(int(self.end_yyyy), int(self.end_mm), self.end_dd)).prefetch_related('animator', 'village', 'farmer_groups_targeted', 'videoes_screened', 'farmers_attendance', 'partner')

    def get_req_id_vrp(self):
        list_of_vrps_in_block2 = self.Screening_all_object.values_list('animator__name','animator__id').distinct()
        return list_of_vrps_in_block2

    def each_vrp_diss_list(self, vrp_id):
        vrp_wise_diss_list = self.Screening_all_object.filter(animator_id = vrp_id)
        return vrp_wise_diss_list

    def get_grp_ids(self,diss_id):
        diss_wise_grp_list = self.Screening_all_object.filter(id=diss_id).values_list('farmer_groups_targeted__id',flat=True)
        return diss_wise_grp_list

    def get_video_shown_list(self,diss_id):
        video_shown_list = []
        video_shown_list = self.Screening_all_object.filter(id=diss_id).values_list('videoes_screened__id',flat=True)
        return video_shown_list

    def get_adoption_data(self, vid_id, attendees):
        self.adoption_list = PersonAdoptPractice.objects.filter(video_id=vid_id, person_id__in=attendees).prefetch_related('video', 'person', 'partner')

    def get_new_adoption_list(self, diss_date):
        self.d_date_yyyy = diss_date.year
        self.d_date_mm = diss_date.month
        self.d_date_dd = diss_date.day
        new_adoption_list = self.adoption_list.filter(date_of_adoption__gt=datetime.date(self.d_date_yyyy, self.d_date_mm, self.d_date_dd),date_of_adoption__lte=datetime.date(self.d_date_yyyy, self.d_date_mm, self.d_date_dd)+datetime.timedelta(weeks=6))
        return new_adoption_list

    def get_old_adoption_list(self, diss_date):
        self.d_date_yyyy = diss_date.year
        self.d_date_mm = diss_date.month
        self.d_date_dd = diss_date.day
        old_adoption_list = self.adoption_list.filter( date_of_adoption__gt=datetime.date(self.d_date_yyyy, self.d_date_mm, self.d_date_dd)-datetime.timedelta(weeks=8), date_of_adoption__lt=datetime.date(self.d_date_yyyy, self.d_date_mm,self.d_date_dd))
        return old_adoption_list

    def get_diss_attendees(self,diss_id):
        self.attendees_list = PersonMeetingAttendance.objects.filter(screening_id=diss_id).values_list('person__id', flat=True)
        return self.attendees_list

    def get_expected_attendance(self,dissemination_grp_id):
        return Person.objects.filter(group_id__in=dissemination_grp_id)

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
    verification_status = models.IntegerField(max_length=1, choices=ADOPTION_VERIFICATION, default=0)

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