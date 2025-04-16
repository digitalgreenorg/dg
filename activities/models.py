# python imports
import calendar
import datetime
# django imports
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.forms import ValidationError
# app imports
from coco.data_log import delete_log, save_log
from coco.base_models import (ADOPTION_VERIFICATION, ADOPT_PRACTICE_CATEGORY, SCREENING_OBSERVATION, SCREENING_GRADE,
                               VERIFIED_BY, TYPE_OF_VENUE, TYPE_OF_VIDEO, TOPICS, ACTIVITY_CHOICES, VIDEO_RELEVANCE_CHOICES, NON_ADOPTION_REASON_CHOICES,
                                DISSEMINATION_CHALLENGES_CHOICES, PARTICIPATION_DISCOMFORT_REASONS_CHOICES, YES_NO_CHOICES,
                                LOCATION_CONVENIENCE_CHOICES, TIME_CONVENIENCE_CHOICES, NNG_RECALL_CHOICES, CocoModel)
from geographies.models import Village
from programs.models import Partner
from people.models import Animator, JSLPS_Animator, AP_Animator, JSLPS_Person, Person, PersonGroup
from videos.models import Video, JSLPS_Video, APVideo, APPractice, ParentCategory


class VRPpayment(models.Manager):

    "Custom manager filters standard query set with given args."
    def __init__(self, partner_id, block_id, start_period, end_period):
        super(VRPpayment, self).__init__()
        self.start_yyyy = start_period[-4:]
        self.start_mm = start_period[:2]
        self.start_dd = 01
        self.end_yyyy = end_period[-4:]
        self.end_mm = end_period[:2]
        self.end_dd = calendar.monthrange(int(self.end_yyyy),int(self.end_mm))[1]
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


class FrontLineWorkerPresent(models.Model):
    worker_type = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.worker_type

class Screening(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    parentcategory = models.ForeignKey(ParentCategory, null=True, blank=True)
    village = models.ForeignKey(Village)
    animator = models.ForeignKey(Animator)
    farmer_groups_targeted = models.ManyToManyField(PersonGroup)
    videoes_screened = models.ManyToManyField(Video)
    questions_asked = models.TextField(null=True, blank=True)
    farmers_attendance = models.ManyToManyField(Person, through='PersonMeetingAttendance')
    partner = models.ForeignKey(Partner)
    observation_status = models.IntegerField(choices=SCREENING_OBSERVATION, default=0, validators=[MaxValueValidator(1)])
    screening_grade = models.CharField(max_length=1,choices=SCREENING_GRADE,null=True,blank=True)
    observer = models.IntegerField( choices=VERIFIED_BY, null=True, blank=True, validators=[MaxValueValidator(2)])
    health_provider_present = models.BooleanField(default=False)
    # UPAVAN fields
    type_of_video = models.CharField(max_length=20, choices=TYPE_OF_VIDEO, null=True, blank=True)
    frontlineworkerpresent =  models.ManyToManyField(FrontLineWorkerPresent, blank=True)
    type_of_venue = models.CharField(choices=TYPE_OF_VENUE,
                                     blank=True, null=True,
                                     max_length=40)
    meeting_topics = models.CharField(choices=TOPICS,
                                     blank=True, null=True,
                                     max_length=255)

    class Meta:
        unique_together = ("date", "start_time", "end_time", "animator", "village")

    def __unicode__(self):
        return u'%s' % (self.village.village_name)

    def screening_location(self):
        return u'%s (%s) (%s) (%s)' % (self.village.village_name, self.village.block.block_name, self.village.block.district.district_name, self.village.block.district.state.state_name)

post_save.connect(save_log, sender=Screening)
pre_delete.connect(delete_log, sender=Screening)


class PersonMeetingAttendance(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    screening = models.ForeignKey(Screening)
    person = models.ForeignKey(Person)
    category = models.CharField(max_length=80, null=True)
    
    def __unicode__(self):
        return  u'%s' % (self.id)


class FarmerFeedback(CocoModel):
    """
    Model for capturing farmer feedback during video dissemination sessions.
    """
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    screening = models.ForeignKey(
        Screening, on_delete=models.CASCADE,
        help_text="The dissemination session this feedback relates to"
    )
    videos = models.ManyToManyField(
        Video, through='FarmerFeedbackVideo', help_text="The videos shown during the session"
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        help_text="The farmer providing the feedback"
    )
    # Feedback on the relevance of the video
    video_relevance = models.CharField(
        max_length=20,
        choices=VIDEO_RELEVANCE_CHOICES,
        help_text="How relevant was the video?"
    )
    # Confidence in adopting the practice
    adoption_confidence = models.CharField(
        max_length=20,
        choices=YES_NO_CHOICES,
        help_text="Does the farmer feel confident in adopting the practice?"
    )
    # Reasons for not adopting (if any)
    non_adoption_reasons = models.CharField(
        max_length=2,  # corrected from 'mas_length'
        choices=NON_ADOPTION_REASON_CHOICES,
        blank=True,
        null=True,
        help_text="If No, Why?"
    )
    non_adoption_reasons_other = models.TextField(
        blank=True,
        null=True,
        help_text="If not confident, reasons for not adopting (e.g., clarity, accessibility, cost, risk, etc.)"
    )
    # Feedback on logistics
    location_convenience = models.CharField(
        max_length=20,
        choices=LOCATION_CONVENIENCE_CHOICES,
        help_text="Feedback on the dissemination location"
    )
    location_convenience_other = models.TextField(
        blank=True,
        null=True,
        help_text="Additional details about location convenience"
    )
    time_convenience = models.CharField(
        max_length=20,
        choices=YES_NO_CHOICES,
        help_text="Was the screening time convenient?"
    )
    convenient_time = models.CharField(
        max_length=20,
        choices=TIME_CONVENIENCE_CHOICES,
        blank=True,
        null=True,
        help_text="If the screening time was not convenient, which alternative time is preferred?"
    )
    additional_challenges_encountered = models.CharField(
        max_length=20,
        choices=YES_NO_CHOICES,
        help_text="Do you face any additional challenges in attending video dissemination sessions other than time and location?"
    )
    additional_challenges = models.CharField(
        max_length=20,
        choices=DISSEMINATION_CHALLENGES_CHOICES,
        blank=True,
        null=True,
        help_text="If yes, what are the potential problems?"
    )
    additional_challenges_other = models.TextField(
        blank=True,
        null=True,
        help_text="Additional details for challenges encountered"
    )
    # Feedback on participation during the session
    comfortable_asking = models.CharField(
        max_length=20,
        choices=YES_NO_CHOICES,
        help_text="Did the farmer feel comfortable asking questions and participating?"
    )
    asking_discomfort_reasons = models.CharField(
        max_length=2,
        choices=PARTICIPATION_DISCOMFORT_REASONS_CHOICES,
        blank=True,
        null=True,
        help_text="If not comfortable, what were the reasons?"
    )
    asking_discomfort_reasons_other = models.TextField(
        blank=True,
        null=True,
        help_text="If not comfortable, please specify other reasons"
    )
    # Overall recommendation and recall of key video points
    recommendation_rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)],
        help_text="On a scale of 0-10, how likely is the farmer to recommend the practice?"
    )
    nng_recall = models.CharField(
        max_length=20,
        choices=NNG_RECALL_CHOICES,
        help_text="Farmer's recall of the main (non-negotiable) points in the video"
    )
    # Open ended suggestions for future video topics/practices
    suggestions = models.TextField(
        blank=True,
        null=True,
        help_text="Other agricultural practices or topics the farmer would like to see in videos"
    )
    
    def __unicode__(self):
        videos = self.videos.all()
        video_titles = ", ".join([v.title for v in videos]) if videos else "no videos"
        return u"Feedback by %s on [%s] at %s" % (self.person.person_name, video_titles, self.screening.date)

    class Meta:
        verbose_name = "Farmer Feedback"
        verbose_name_plural = "Farmer Feedbacks"

# Connect signals for logging
models.signals.post_save.connect(save_log, sender=FarmerFeedback)
models.signals.pre_delete.connect(delete_log, sender=FarmerFeedback)

class FarmerFeedbackVideo(CocoModel):
    id = models.AutoField(primary_key=True)
    farmerfeedback = models.ForeignKey("FarmerFeedback", on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="The video shown during the session")

    class Meta:
        unique_together = (("farmerfeedback", "video"),)
        verbose_name = "Farmer Feedback Video"


class PersonAdoptPractice(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    person = models.ForeignKey(Person)
    video = models.ForeignKey(Video)
    animator = models.ForeignKey(Animator)
    date_of_adoption = models.DateField()
    date_of_verification = models.DateField(null=True, blank=True)
    partner = models.ForeignKey(Partner)
    verification_status = models.IntegerField(choices=ADOPTION_VERIFICATION, default=0, validators=[MaxValueValidator(2)])
    non_negotiable_check = models.CharField(max_length=256, blank=True, null=True)
    verified_by = models.IntegerField(choices=VERIFIED_BY, null=True, blank=True, validators=[MaxValueValidator(2)])
    parentcategory = models.ForeignKey(ParentCategory, null=True, blank=True)
    adopt_practice = models.CharField(max_length=1, choices=ADOPT_PRACTICE_CATEGORY, null=True, blank=True)
    adopt_practice_second = models.CharField(max_length=1, choices=ADOPT_PRACTICE_CATEGORY, null=True, blank=True)
    krp_one = models.BooleanField(verbose_name="1", db_index=True, default=False)
    krp_two = models.BooleanField(verbose_name="2", db_index=True, default=False)
    krp_three = models.BooleanField(verbose_name="3", db_index=True,default=False)
    krp_four = models.BooleanField(verbose_name="4", db_index=True, default=False)
    krp_five = models.BooleanField(verbose_name="5", db_index=True, default=False)

    def __unicode__(self):
        return "%s (%s) (%s) (%s) (%s)" % (self.person.person_name, self.person.father_name, self.person.group.group_name if self.person.group else '', self.person.village.village_name, self.video.title)

    def clean(self):
        super(PersonAdoptPractice, self).clean()
        # Only run this if we have person, video, and date_of_adoption
        if self.person_id and self.video_id and self.date_of_adoption:
            window_start = self.date_of_adoption - datetime.timedelta(days=30)
            window_end   = self.date_of_adoption + datetime.timedelta(days=30)
            qs = PersonAdoptPractice.objects.filter(
                person=self.person_id,
                video=self.video_id,
                date_of_adoption__gte=window_start,
                date_of_adoption__lte=window_end
            )
            # exclude self if updating
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("An adoption for the same person (%s) & video (%s) already exists within 30 days." % (self.person.person_name, self.video.title))
    class Meta:
        unique_together = ("person", "video", "date_of_adoption")

post_save.connect(save_log, sender=PersonAdoptPractice)
pre_delete.connect(delete_log, sender=PersonAdoptPractice)

class JSLPS_Screening(CocoModel):
    id = models.AutoField(primary_key=True)
    screenig_code = models.CharField(max_length=100)
    screening = models.ForeignKey(Screening, null=True, blank=True)
    farmers_attendance = models.ManyToManyField(JSLPS_Person,
                                                through='JSLPS_PersonMeetingAttendance',
                                                blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS Screening"
        verbose_name_plural = "JSLPS Screening"


class JSLPS_PersonMeetingAttendance(CocoModel):
    screening = models.ForeignKey(JSLPS_Screening)
    person = models.ForeignKey(JSLPS_Person)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)
    
    def __unicode__(self):
        return  u'%s' % (self.id)


class JSLPS_Adoption(CocoModel):
    id = models.AutoField(primary_key=True)
    member_code = models.CharField(max_length=100)
    jslps_video = models.ForeignKey(JSLPS_Video)
    jslps_date_of_adoption = models.DateField()
    jslps_akmcode = models.ForeignKey(JSLPS_Animator)
    adoption = models.ForeignKey(PersonAdoptPractice, null=True, blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS Adoption"
        verbose_name_plural = "JSLPS Adoption"



class AP_Screening(CocoModel):
    screening_code = models.CharField(max_length=100)
    screening = models.ForeignKey(Screening, null=True, blank=True)
    no_of_male = models.CharField(max_length=100, null=True)
    no_of_female = models.CharField(max_length=100, null=True)
    total_members = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Screening"
        verbose_name_plural = "Screening"


class AP_Adoption(CocoModel):
    member_code = models.CharField(max_length=255)
    member_name = models.CharField(max_length=255)
    ap_video = models.ForeignKey(APVideo, null=True, blank=True)
    date_of_adoption = models.DateField()
    ap_animator = models.ForeignKey(AP_Animator)
    adoption = models.ForeignKey(PersonAdoptPractice, null=True, blank=True)
    ap_adopt_practice = models.ForeignKey(APPractice, null=True, blank=True)
    adoption_type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Adoption"
        verbose_name_plural = "Adoption"


