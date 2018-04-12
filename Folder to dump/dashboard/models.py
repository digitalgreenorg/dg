#===============================================================================
# import datetime
# import sys
# import traceback
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.mail import send_mail
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db import models
# from django.db.models import Min, Count, F
# from django.db.models.signals import m2m_changed, pre_delete, post_delete, pre_save, post_save
# from dashboard.fields import BigAutoField, BigForeignKey, BigManyToManyField, PositiveBigIntegerField 
# from coco.data_log import delete_log, save_log
# from libs.geocoder import Geocoder
# 
# import logging
# import sys, traceback, datetime
# 
# 
# # Variables
# GENDER_CHOICES = (
#     ('M', 'Male'),
#     ('F', 'Female'),
# )
# 
# SEASONALITY = (
#         ('Jan','January'),
#         ('Feb','February'),
#         ('Mar','March'),
#         ('Apr','April'),
#         ('May','May'),
#         ('Jun','June'),
#         ('Jul','July'),
#         ('Aug','August'),
#         ('Sep','September'),
#         ('Oct','October'),
#         ('Nov','November'),
#         ('Dec','December'),
#         ('Kha','Kharif'),
#         ('Rab','Rabi'),
#         ('Rou','Round the year'),
#         ('Rai','Rainy season'),
#         ('Sum','Summer season'),
#         ('Win','Winter season'),
# )
# 
# VIDEO_TYPE = (
#         (1,'Demonstration'),
#         (2,'Success story/ Testimonial'),
#         (3,'Activity Introduction'),
#         (4,'Discussion'),
#         (5,'General Awareness'),
# )
# 
# STORYBASE = (
#         (1,'Agricultural'),
#         (2,'Institutional'),
#     (3,'Health'),
# )
# 
# ACTORS = (
#         ('I','Individual'),
#         ('F','Family'),
#         ('G','Group'),
# )
# 
# SUITABLE_FOR = (
#         (1,'Dissemination'),
#         (2,'Video Production Training'),
#         (3,'Dissemination Training'),
#         (4,'Nothing'),
#         (5,'Pending for Approval'),
# )
# 
# ROLE = (
#         ('F','Field Officer'),
#         ('D', 'Development Manager'),
#         ('A', 'Administrator'),
# )
# 
# EQUIPMENT = (
#              (1,'Pico Projector'),
#              (2,'Speaker'),
#              (3,'Camera'),
#              (4,'Tripod'),
#              (5,'Battery'),
#              (6,'Battery Charger'),
#              (7,'Laptop'),
#              (8,'Computer'),
#              (9,'Television set'),
#              (10,'DVD player'),
#              (11,'Headphone'),
#              (12,'Microphone'),
#              (13,'Hard disk'),
#              (14,'Pen drive'),
#              (15,'UPS'),
#              (16,'Cycle'),
#              (17,'Chair'),
#              (18,'Table'),
#              (19,'Almirah'),
#              (20,'Bag'),
#              (21,'Other'),
# )
# 
# EQUIPMENT_PURPOSE = (
#                      (1,'DG Delhi office'),
#                      (2,'DG Bangalore office'),
#                      (3,'DG Bhopal office'),
#                      (4,'DG Bhubaneswar office'),
#                      (5,'Partners office'),
#                      (6,'Field'),
#                      (7,'Individual'),
# )
# 
# class ServerLog(models.Model):
#     id = BigAutoField(primary_key=True)
#     timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
#     user = models.ForeignKey(User, null = True)
#     village = models.BigIntegerField(null = True)
#     action = models.IntegerField()
#     entry_table = models.CharField(max_length=100)
#     model_id = models.BigIntegerField(null = True)
#     partner = models.BigIntegerField(null = True)
#     
# #    def __unicode__(self):
# #        return self.entry_table
# 
# class CocoModel(models.Model):
#     user_created = models.ForeignKey(User, related_name ="%(class)s_created", editable = False, null=True, blank=True)
#     time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     user_modified = models.ForeignKey(User, related_name ="%(class)s_related_modified",editable = False, null=True, blank=True)
#     time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
#   
#     class Meta:
#         abstract = True
# 
#     def get_village(self):
#         return self.village.id
#     def get_partner(self):
#         return self.village.block.district.partner.id
# 
# class OfflineUserManager(models.Manager):
#     def get_offline_pk(self, username, flag_create):
#         """
#         username, flag_create
#         """
#         user = User.objects.get(username=username)
#         if user is None:
#             # Log "Anonymous User Access"
#             return None
#         try:
#             offline_user = OfflineUser.objects.get(user=user)
#         except ObjectDoesNotExist:
#             if flag_create:
#                 BILLION_CONSTANT = 1000000000
#                 offline_id = (int(user.id) * BILLION_CONSTANT) + 1000
#                 offline_user = OfflineUser()
#                 offline_user.user = user
#                 offline_user.offline_pk_id = offline_id
#                 offline_user.save()
#             else:
#                 return None
#         return offline_user.offline_pk_id
#     
#     def set_offline_pk(self, offline_pk):
#         user_id = int(offline_pk)/1000000000
#         if user_id < 1:
#             # Log generated id does not correspond to the correct format
#             return False
#         user = User.objects.get(id=user_id)
#         if user is None:
#             # Log "Anonymous User Access"
#             return False
#         try:
#             offline_user = OfflineUser.objects.get(user=user)
#         except ObjectDoesNotExist:
#             return False
#         min_auto_increment = 10000000000000
#         if offline_pk > min_auto_increment or offline_user.offline_pk_id > offline_pk:
#             # LOG THIS -> SOME MAJOR GHAPLA HAS OCCURED
#             return False
#         offline_user.offline_pk_id = offline_pk
#         offline_user.save()
#         return True
# 
# class OfflineUser(CocoModel):
#     user = models.ForeignKey(User)
#     offline_pk_id = PositiveBigIntegerField()
#     objects = OfflineUserManager()
#     
# class RegionTest(CocoModel):
#     region_name = models.CharField(max_length=100, db_column='REGION_NAME', unique='True')
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     id = models.AutoField(primary_key=True, db_column = 'id')
#     class Meta:
#         db_table = u'region_test'
# 
#     def __unicode__(self):
#         return self.region_name
# 
# class Region(CocoModel):
#     id = BigAutoField(primary_key = True)
#     region_name = models.CharField(max_length=100, db_column='REGION_NAME', unique='True')
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     class Meta:
#         db_table = u'region'
# 
#     def __unicode__(self):
#         return self.region_name
#     
# class Country(CocoModel):
#     id = BigAutoField(primary_key = True)
#     country_name = models.CharField(max_length=100, db_column='COUNTRY_NAME', unique='True')
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     
#     class Meta:
#         db_table = u'country'
#         verbose_name_plural = "countries"
# 
#     def __unicode__(self):
#         return self.country_name
# 
# class EquipmentHolder(CocoModel):
#     id = BigAutoField(primary_key = True)
#     content_type = models.ForeignKey(ContentType)
#     object_id = PositiveBigIntegerField()
#     content_object = generic.GenericForeignKey("content_type", "object_id")
#     class Meta:
#         db_table = u'equipment_holder'
# 
#     def __unicode__(self):
#         return u'%s' % self.content_object
# 
# class Reviewer(CocoModel):
#     id = BigAutoField(primary_key = True)
#     content_type = models.ForeignKey(ContentType)
#     object_id = PositiveBigIntegerField()
#     content_object = generic.GenericForeignKey("content_type", "object_id")
#     class Meta:
#         db_table = u'reviewer'
# 
#     def __unicode__(self):
#         return u'%s' % self.content_object
# 
# 
# class DevelopmentManager(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=100, db_column='NAME')
#     age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER')
#     hire_date = models.DateField(null=True, db_column='HIRE_DATE', blank=True)
#     phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True)
#     address = models.CharField(max_length=500, db_column='ADDRESS', blank=True)
#     speciality = models.TextField(db_column='SPECIALITY', blank=True)
#     region =  BigForeignKey(Region)
#     start_day = models.DateField(null=True, db_column='START_DAY', blank=True)
#     salary = models.FloatField(null=True, db_column='SALARY', blank=True)
#     class Meta:
#         db_table = u'development_manager'
# 
#     def __unicode__(self):
#         return self.name
# 
# class State(CocoModel):
#     id = BigAutoField(primary_key = True)
#     state_name = models.CharField(max_length=100, db_column='STATE_NAME', unique='True')
#     region = BigForeignKey(Region)
#     country = BigForeignKey(Country)
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     class Meta:
#         db_table = u'state'
# 
#     def __unicode__(self):
#         return self.state_name
# 
# class Partners(CocoModel):
#     id = BigAutoField(primary_key = True)
#     partner_name = models.CharField(max_length=100, db_column='PARTNER_NAME')
#     date_of_association = models.DateField(null=True, db_column='DATE_OF_ASSOCIATION', blank=True)
#     phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True)
#     address = models.CharField(max_length=500, db_column='ADDRESS', blank=True)
# 
#     class Meta:
#         db_table = u'partners'
#         verbose_name = "Partner"
# 
# 
#     def __unicode__(self):
#         return self.partner_name
# 
# class FieldOfficer(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=100, db_column='NAME')
#     age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER')
#     hire_date = models.DateField(null=True, db_column='HIRE_DATE', blank=True)
#     salary = models.FloatField(null=True, db_column='SALARY', blank=True)
#     phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True)
#     address = models.CharField(max_length=500, db_column='ADDRESS', blank=True)
# 
#     class Meta:
#         db_table = u'field_officer'
# 
#     def __unicode__(self):
#         return self.name
# 
# class District(CocoModel):
#     id = BigAutoField(primary_key = True)
#     district_name = models.CharField(max_length=100, db_column='DISTRICT_NAME', unique='True')
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     state = BigForeignKey(State)
#     fieldofficer = BigForeignKey(FieldOfficer)
#     fieldofficer_startday = models.DateField(null=True, db_column='FIELDOFFICER_STARTDAY', blank=True)
#     partner = BigForeignKey(Partners)
#     latitude = models.DecimalField(max_digits=31, decimal_places=28, null=True, blank=True,
#                                    validators=[MaxValueValidator(90), MinValueValidator(-90)])
#     longitude = models.DecimalField(max_digits=32, decimal_places=28, null=True, blank=True,
#                                     validators=[MaxValueValidator(180), MinValueValidator(-180)])
# 
#     class Meta:
#         db_table = u'district'
# 
#     def __unicode__(self):
#         return self.district_name
# 
#     def clean(self):
#         logger = logging.getLogger('dashboard')
#         if(self.latitude is None or self.longitude is None):
#             geocoder = Geocoder()
#             address = u"%s,%s,%s" % (self.district_name, self.state.state_name, self.state.country.country_name)
#             if (geocoder.convert(address)):
#                 try:
#                     (self.latitude, self.longitude) = geocoder.getLatLng()
#                     logger.info("%s: Lat Long Added" % self.district_name)
#                 except:
#                     logger.error("Geocodes not found for %s, %s" % (self.district_name, self.state.state_name))
#                   
# class Block(CocoModel):
#     id = BigAutoField(primary_key = True)
#     block_name = models.CharField(max_length=100, db_column='BLOCK_NAME', unique='True')
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     district = BigForeignKey(District)
#     class Meta:
#         db_table = u'block'
# 
#     def __unicode__(self):
#         return self.block_name
# 
# class VillageFarmerbookManager(models.Manager):
#     def get_query_set(self):
#         return super(VillageFarmerbookManager, self).get_query_set().filter(person__image_exists=True).distinct()
# 
# class Village(CocoModel):
#     id = BigAutoField(primary_key = True)
#     village_name = models.CharField(max_length=100, db_column='VILLAGE_NAME')
#     block = BigForeignKey(Block)
#     no_of_households = models.IntegerField(null=True, db_column='NO_OF_HOUSEHOLDS', blank=True)
#     population = models.IntegerField(null=True, db_column='POPULATION', blank=True)
#     road_connectivity = models.CharField(max_length=100, db_column='ROAD_CONNECTIVITY', blank=True)
#     control = models.NullBooleanField(null=True, db_column='CONTROL', blank=True)
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     latitude = models.CharField(max_length=25, null=True, blank=True)
#     longitude = models.CharField(max_length=25, null=True, blank=True)
#     grade = models.CharField(max_length=1, null=True, blank=True)
#     objects = models.Manager() #The default manager
#     farmerbook_village_objects = VillageFarmerbookManager() #The manager for farmerbook
#     
#     class Meta:
#         db_table = u'village'
#         unique_together = ("village_name","block")
# 
#     def get_village(self):
#         return self.id
#     def get_partner(self):
#         return self.block.district.partner.id
#     
#     def __unicode__(self):
#         return self.village_name
# post_save.connect(save_log, sender = Village)
# pre_delete.connect(delete_log, sender = Village)
# 
# class MonthlyCostPerVillage(CocoModel):
#     id = BigAutoField(primary_key = True)
#     village = BigForeignKey(Village)
#     date = models.DateField(db_column='DATE')
#     labor_cost = models.FloatField(null=True, db_column='LABOR_COST', blank=True)
#     equipment_cost = models.FloatField(null=True, db_column='EQUIPMENT_COST', blank=True)
#     transportation_cost = models.FloatField(null=True, db_column='TRANSPORTATION_COST', blank=True)
#     miscellaneous_cost = models.FloatField(null=True, db_column='MISCELLANEOUS_COST', blank=True)
#     total_cost = models.FloatField(null=True, db_column='TOTAL_COST', blank=True)
#     partners_cost = models.FloatField(null=True, db_column='PARTNERS_COST', blank=True)
#     digitalgreen_cost = models.FloatField(null=True, db_column='DIGITALGREEN_COST', blank=True)
#     community_cost = models.FloatField(null=True, db_column='COMMUNITY_COST', blank=True)
#     class Meta:
#         db_table = u'monthly_cost_per_village'
# 
# class PersonGroups(CocoModel):
#     id = BigAutoField(primary_key = True)
#     DAY_CHOICES = (
#                 ('Monday','Monday'),
#                 ('Tuesday','Tuesday'),
#                 ('Wednesday','Wednesday'),
#                 ('Thursday','Thursday'),
#                 ('Friday','Friday'),
#                 ('Saturday','Saturday'),
#                 ('Sunday','Sunday'),
#                   )
#     group_name = models.CharField(max_length=100, db_column='GROUP_NAME')
#     days = models.CharField(max_length=9,choices=DAY_CHOICES, db_column='DAYS', blank=True)
#     timings = models.TimeField(db_column='TIMINGS',null=True, blank=True)
#     time_updated = models.DateTimeField(db_column='TIME_UPDATED',auto_now=True)
#     village = BigForeignKey(Village)
#     partner = BigForeignKey(Partners)
#     class Meta:
#         db_table = u'person_groups'
#         verbose_name = "Person group"
#         unique_together = ("group_name", "village")
# 
#     def __unicode__(self):
#         return  u'%s (%s)' % (self.group_name, self.village)
#         #return self.group_name
# post_save.connect(save_log, sender = PersonGroups)
# pre_delete.connect(delete_log, sender = PersonGroups)
# 
# class FarmerbookManager(models.Manager):
#     def get_query_set(self):
#         return super(FarmerbookManager, self).get_query_set().filter(image_exists=True)
# 
# class Person(CocoModel):
#     id = BigAutoField(primary_key = True)
#     person_name = models.CharField(max_length=100, db_column='PERSON_NAME')
#     father_name = models.CharField(max_length=100, db_column='FATHER_NAME', blank=True)
#     age = models.IntegerField(max_length=3, null=True, db_column='AGE', blank=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_column='GENDER')
#     phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True)
#     address = models.CharField(max_length=500, db_column='ADDRESS', blank=True)
#     land_holdings = models.FloatField(null=True, db_column='LAND_HOLDINGS', blank=True)
#     village = BigForeignKey(Village)
#     group = BigForeignKey(PersonGroups, null=True, blank=True)
#     relations = models.ManyToManyField('self', symmetrical=False, through='PersonRelations',related_name ='rel',null=True,blank=True)
#     date_of_joining = models.DateField(null=True, blank=True)
#     #changes done for farmerbook. one new Boolean field image_exists added
#     image_exists = models.BooleanField(default=False)
#     
#     objects = models.Manager() #The default manager
#     farmerbook_objects = FarmerbookManager() #The manager for farmerbook
#     partner = BigForeignKey(Partners)
#     
#     class Meta:
#         db_table = u'person'
#         unique_together = ("person_name", "father_name", "village")
#         
#     # Called on any update/insert/delete of PersonMeetingAttendance/PersonShownInVideo
#     @staticmethod
#     def date_of_joining_handler(sender, **kwargs):
#         try:
#             def get_min_date(person, exclude_model, exclude_pk_set):
#                 all_dates = []
#                 if exclude_model == Screening:
#                     all_dates.extend(person.screening_set.exclude(id__in = exclude_pk_set).values_list('date',flat=True))
#                 else:
#                     all_dates.extend(person.screening_set.values_list('date',flat=True))
#                 
#                 if exclude_model == Video:
#                     all_dates.extend(person.video_set.exclude(id__in = exclude_pk_set).values_list('video_production_end_date',flat=True))
#                 else:
#                     all_dates.extend(person.video_set.values_list('video_production_end_date',flat=True))
#                 
#                 if all_dates:
#                     return min(all_dates);
#                 else:
#                     return None
#                     
#             instance = kwargs['instance']
#             if sender == Screening or sender == Video:
#                 if kwargs['signal'] == pre_save and instance.pk != None:
#                     if(sender == Screening):
#                         old_date_vqs = Screening.objects.filter(pk=instance.pk).values('date')
#                         if(not bool(old_date_vqs)):
#                             return
#                         old_date = old_date_vqs[0]['date']
#                         person_set = instance.farmers_attendance.all()
#                         check_date = instance.date
#                     elif sender == Video:
#                         old_date_vqs = Video.objects.filter(pk=instance.pk).values('video_production_end_date')
#                         if(not bool(old_date_vqs)):
#                             return
#                         old_date = old_date_vqs[0]['video_production_end_date']
#                         person_set = instance.farmers_shown.all()
#                         check_date = instance.video_production_end_date
#                     if old_date == check_date:
#                         return
#                     for person in person_set:
#                         if person.date_of_joining == None:
#                             continue 
#                         if check_date < person.date_of_joining:
#                             person.date_of_joining = check_date
#                             person.save()
#                         elif person.date_of_joining == old_date:
#                             person.date_of_joining = min(filter(lambda x: x is not None, [check_date, get_min_date(person, sender, (instance.pk,))]))
#                             person.save()
#                 elif kwargs['signal'] == pre_delete:
#                     if sender == Video:
#                         person_set = instance.farmers_shown.all()
#                         check_date = instance.video_production_end_date
#                     for person in person_set:
#                         if person.date_of_joining == None:
#                             continue
#                         if check_date == person.date_of_joining:
#                             min_date = get_min_date(person, sender, (instance.pk,))
#                             if min_date != person.date_of_joining:
#                                 person.date_of_joining = min_date
#                                 person.save()
#             elif sender == PersonMeetingAttendance:
#                 if kwargs['signal'] == pre_save:
#                     if instance.pk != None:
#                         old_pma_qs = PersonMeetingAttendance.objects.filter(pk=instance.pk)
#                     if(instance.pk == None or not bool(old_pma_qs)):
#                         person = Person.objects.get(pk=instance.person.pk)
#                         if person.date_of_joining == None or person.date_of_joining > instance.screening.date:
#                             person.date_of_joining = instance.screening.date
#                             person.save()
#                     else:
#                         old_pma = old_pma_qs[0]
#                         if old_pma.person != instance.person or old_pma.screening != instance.screening:
#                             old_person = old_pma.person
#                             min_vid_date = (old_person.video_set.aggregate(Min('video_production_end_date'))).values()[0]
#                             min_sc_date = (old_person.personmeetingattendance_set.exclude(pk=instance.pk).aggregate(Min('screening__date'))).values()[0]
#                             if min_vid_date or min_sc_date:
#                                 old_person.date_of_joining = min(filter(lambda x: x is not None, [min_vid_date, min_sc_date]))
#                             else:
#                                 old_person.date_of_joining = None
#                             old_person.save()
#                             person = Person.objects.get(pk=instance.person.pk)
#                             if person.date_of_joining == None or person.date_of_joining > instance.screening.date:
#                                 person.date_of_joining = instance.screening.date
#                                 person.save()
#                 elif kwargs['signal'] == post_delete:
#                     try:
#                         #This is put under try..except because if person is deleted, it will cascade delete of PersonMeetingAttendance, get will throw DoesNotExist error
#                         person = Person.objects.get(pk=instance.person.pk)
#                     except ObjectDoesNotExist:
#                         return
#                     try:
#                         #This is put under try..except because if Screening is deleted, it will cascade delete of PersonMeetingAttendance, get will throw DoesNotExist error
#                         date = instance.screening.date
#                     except ObjectDoesNotExist:
#                         min_date = get_min_date(person, Screening, (instance.screening_id,))
#                         if min_date != person.date_of_joining:
#                             person.date_of_joining = min_date
#                             person.save()
#                     else:
#                         if(person.date_of_joining == date):
#                             min_vid_date = (person.video_set.aggregate(Min('video_production_end_date'))).values()[0]
#                             min_sc_date = (person.personmeetingattendance_set.exclude(pk=instance.pk).aggregate(Min('screening__date'))).values()[0]
#                             if min_vid_date or min_sc_date:
#                                 person.date_of_joining = min(filter(lambda x: x is not None, [min_vid_date, min_sc_date]))
#                             else:
#                                 person.date_of_joining = None
#                             person.save()
#             elif sender == Video.farmers_shown.through:
#                 if kwargs['reverse'] == False:
#                     person_set = instance.farmers_shown.all()
#                     check_date = instance.video_production_end_date
#                     if kwargs['action'] == 'pre_clear' or kwargs['action'] == 'pre_remove':
#                         if kwargs['action'] == 'pre_remove':
#                             person_set = Person.objects.filter(id__in = kwargs['pk_set'])
#                         for person in person_set:
#                             if check_date == person.date_of_joining:
#                                 min_date = get_min_date(person, instance.__class__, (instance.pk,))
#                                 if min_date != person.date_of_joining:
#                                     person.date_of_joining = min_date
#                                     person.save()
#                     elif kwargs['action'] == 'post_add':
#                         person_set = Person.objects.filter(id__in = kwargs['pk_set'])
#                         for person in person_set:    
#                             if person.date_of_joining == None or check_date < person.date_of_joining:
#                                 person.date_of_joining = check_date
#                                 person.save()
#                 else:
#                     if kwargs['action'] == 'pre_clear':
#                         min_date = (instance.screening_set.aggregate(Min('date'))).values()[0]
#                         if min_date != instance.date_of_joining:
#                             instance.date_of_joining = min_date
#                             instance.save()
#                     elif kwargs['action'] == 'pre_remove':
#                         check_date = (Video.objects.filter(pk__in = kwargs['pk_set']).aggregate(Min('video_production_end_date'))).values()[0]
#                         if check_date == instance.date_of_joining:
#                             min_date = get_min_date(instance, kwargs['model'], kwargs['pk_set'])
#                             if min_date != instance.date_of_joining:
#                                 instance.date_of_joining = min_date
#                                 instance.save()
#                     elif kwargs['action'] == 'post_add':
#                         check_date = (Video.objects.filter(pk__in = kwargs['pk_set']).aggregate(Min('video_production_end_date'))).values()[0]
#                         if instance.date_of_joining == None or check_date < instance.date_of_joining:
#                             instance.date_of_joining = check_date
#                             instance.save()
#         except Exception:
#             #Catching all to avoid bugs from stopping COCO
#             #Sending email to rahul@digitalgreen.org
#             error_type, value, tracebk = sys.exc_info()
#             mail_body = str(type)+":"+str(value)+"\n"+str(traceback.extract_tb(tracebk))
#             send_mail("Error in date_of_joining_handler", mail_body,'server@digitalgreen.org',recipient_list=['rahul@digitalgreen.org'])
# 
#     def __unicode__(self):
#         display = "%s" % (self.person_name)
#         display += " (%s)" % self.father_name if self.father_name.strip()!="" else "" 
#         display += " (%s)" % self.group.group_name if self.group is not None else ""
#         display += " (%s)" % self.village.village_name
#         return  display
# post_save.connect(save_log, sender = Person)
# pre_delete.connect(delete_log, sender = Person)
# 
# class PersonRelations(models.Model):
#     id = BigAutoField(primary_key = True)
#     person = BigForeignKey(Person,related_name='person')
#     relative = BigForeignKey(Person,related_name='relative')
#     type_of_relationship = models.CharField(max_length=100, db_column='TYPE_OF_RELATIONSHIP')
#     class Meta:
#         db_table = u'person_relations'
# 
# class Animator(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=100, db_column='NAME')
#     age = models.IntegerField(max_length=3,null=True, db_column='AGE', blank=True)
#     gender = models.CharField(max_length=1,choices=GENDER_CHOICES, db_column='GENDER')
#     csp_flag = models.NullBooleanField(null=True, db_column='CSP_FLAG', blank=True)
#     camera_operator_flag = models.NullBooleanField(null=True, db_column='CAMERA_OPERATOR_FLAG', blank=True)
#     facilitator_flag = models.NullBooleanField(null=True, db_column='FACILITATOR_FLAG', blank=True)
#     phone_no = models.CharField(max_length=100, db_column='PHONE_NO', blank=True)
#     address = models.CharField(max_length=500, db_column='ADDRESS', blank=True)
#     partner = BigForeignKey(Partners)
#     village = BigForeignKey(Village, db_column = 'home_village_id', null=True, blank=True)
#     district = BigForeignKey(District, null = True, blank=True, help_text='Please select this')
#     assigned_villages = models.ManyToManyField(Village, related_name = 'assigned_villages' ,through='AnimatorAssignedVillage',null=True, blank=True)
#     total_adoptions = models.PositiveIntegerField(default=0, blank=True, editable=False) 
#     
#     class Meta:
#         db_table = u'animator'
#         unique_together = ("name", "gender", "partner","district")
# 
#     def get_village(self):
#         return None
#     def get_partner(self):
#         return self.partner.id
#     
#     def __unicode__(self):
#         return  u'%s (%s)' % (self.name, self.village)
#         #return self.name
# post_save.connect(save_log, sender = Animator)
# pre_delete.connect(delete_log, sender = Animator)
# 
# class Training(CocoModel):
#     id = BigAutoField(primary_key = True)
#     training_purpose = models.TextField(db_column='TRAINING_PURPOSE', blank=True)
#     training_outcome = models.TextField(db_column='TRAINING_OUTCOME', blank=True)
#     training_start_date = models.DateField(db_column='TRAINING_START_DATE')
#     training_end_date = models.DateField(db_column='TRAINING_END_DATE')
#     village = BigForeignKey(Village)
#     development_manager_present = BigForeignKey(DevelopmentManager, null=True, blank=True, db_column='dm_id')
#     fieldofficer = BigForeignKey(FieldOfficer, verbose_name="field officer present", db_column='fieldofficer_id')
#     animators_trained = BigManyToManyField(Animator)
#     class Meta:
#         db_table = u'training'
#         unique_together = ("training_start_date", "training_end_date", "village")
# 
# class AnimatorAssignedVillage(CocoModel):
#     id = BigAutoField(primary_key = True)
#     animator = BigForeignKey(Animator)
#     village = BigForeignKey(Village)
#     start_date = models.DateField(null=True, db_column='START_DATE', blank=True)
#     class Meta:
#         db_table = u'animator_assigned_village'
# 
# class AnimatorSalaryPerMonth(CocoModel):
#     id = BigAutoField(primary_key = True)
#     animator = BigForeignKey(Animator)
#     date = models.DateField(db_column='DATE')
#     total_salary = models.FloatField(null=True, db_column='TOTAL_SALARY', blank=True)
#     pay_date = models.DateField(null=True, db_column='PAY_DATE', blank=True)
#     class Meta:
#         db_table = u'animator_salary_per_month'
# 
# class Language(CocoModel):
#     id = BigAutoField(primary_key = True)
#     language_name = models.CharField(max_length=100,  unique='True')
#     class Meta:
#         db_table = u'language'
#     def get_village(self):
#         return None
#     def get_partner(self):
#         return None
#     def __unicode__(self):
#         return self.language_name
# post_save.connect(save_log, sender = Language)
# pre_delete.connect(delete_log, sender = Language)
# 
# 
# class Video(CocoModel):
#     id = BigAutoField(primary_key = True)
#     title = models.CharField(max_length=200, db_column='TITLE')
#     video_type = models.IntegerField(max_length=1, choices=VIDEO_TYPE, db_column='VIDEO_TYPE')
#     duration = models.TimeField(null=True, db_column='DURATION', blank=True)
#     language = BigForeignKey(Language)
#     summary = models.TextField(db_column='SUMMARY', blank=True)
#     picture_quality = models.CharField(max_length=200, db_column='PICTURE_QUALITY', blank=True)
#     audio_quality = models.CharField(max_length=200, db_column='AUDIO_QUALITY', blank=True)
#     editing_quality = models.CharField(max_length=200, db_column='EDITING_QUALITY', blank=True)
#     edit_start_date = models.DateField(null=True, db_column='EDIT_START_DATE', blank=True)
#     edit_finish_date = models.DateField(null=True, db_column='EDIT_FINISH_DATE', blank=True)
#     thematic_quality = models.CharField(max_length=200, db_column='THEMATIC_QUALITY', blank=True)
#     video_production_start_date = models.DateField(db_column='VIDEO_PRODUCTION_START_DATE')
#     video_production_end_date = models.DateField(db_column='VIDEO_PRODUCTION_END_DATE')
#     storybase = models.IntegerField(max_length=1,choices=STORYBASE, db_column='STORYBASE', null=True, blank=True)
#     storyboard_filename = models.FileField(upload_to='storyboard', db_column='STORYBOARD_FILENAME', blank=True)
#     raw_filename = models.FileField(upload_to='rawfile', db_column='RAW_FILENAME', blank=True)
#     movie_maker_project_filename = models.FileField(upload_to='movie_maker_project_file', db_column='MOVIE_MAKER_PROJECT_FILENAME', blank=True)
#     final_edited_filename = models.FileField(upload_to='final_edited_file', db_column='FINAL_EDITED_FILENAME', blank=True)
#     village = BigForeignKey(Village)
#     facilitator = BigForeignKey(Animator,related_name='facilitator')
#     cameraoperator = BigForeignKey(Animator,related_name='cameraoperator')
#     reviewer = BigForeignKey(Reviewer,null=True, blank=True)
#     approval_date = models.DateField(null=True, blank=True, db_column='APPROVAL_DATE')
#     supplementary_video_produced = BigForeignKey('self',null=True, blank=True)
#     video_suitable_for = models.IntegerField(choices=SUITABLE_FOR,db_column='VIDEO_SUITABLE_FOR')
#     remarks = models.TextField(blank=True, db_column='REMARKS')
#     related_practice = BigForeignKey('Practices',blank=True,null=True)
#     farmers_shown = BigManyToManyField(Person)
#     actors = models.CharField(max_length=1,choices=ACTORS,db_column='ACTORS')
#     last_modified = models.DateTimeField(auto_now=True)
#     youtubeid = models.CharField(max_length=20, db_column='YOUTUBEID',blank=True)
#     viewers = models.PositiveIntegerField(default=0, editable=False)
#     partner = BigForeignKey(Partners)
#     
#     @staticmethod
#     def update_viewer_count(sender, **kwargs):
#         try:
#             if sender == Screening.videoes_screened.through and kwargs['signal'] == m2m_changed:
#                 if kwargs['reverse'] == False:
#                     count = kwargs['instance'].farmers_attendance.count()
#                     if kwargs['action'] == "post_remove":
#                         Video.objects.filter(pk__in = kwargs['pk_set']).update(viewers = F("viewers") - count)
#                     elif kwargs['action'] == "post_add":
#                         Video.objects.filter(pk__in = kwargs['pk_set']).update(viewers = F("viewers") + count)
#                     elif kwargs['action'] == 'pre_clear':
#                         kwargs['instance'].videoes_screened.update(viewers = F("viewers") - count)
#                 else:
#                     video = Video.objects.get(pk=kwargs['instance'].pk)
#                     if kwargs['action'] == "post_remove":
#                         video.viewers = video.viewers - (Screening.objects.filter(pk__in = kwargs['pk_set']).aggregate(c = Count('farmers_attendance'))).values()[0]
#                         video.save()
#                     elif kwargs['action'] == "post_add":
#                         video.viewers = video.viewers + (Screening.objects.filter(pk__in = kwargs['pk_set']).aggregate(c = Count('farmers_attendance'))).values()[0]
#                         video.save()
#                     elif kwargs['action'] == "post_clear":
#                         video.viewers = 0
#                         video.save()
#             elif sender == PersonMeetingAttendance:
#                 if kwargs['signal'] == pre_save:
#                     if kwargs['instance'].pk != None:
#                         old_pma_qs = PersonMeetingAttendance.objects.filter(pk=kwargs['instance'].pk)
#                     if(kwargs['instance'].pk == None or not bool(old_pma_qs)):
#                         kwargs['instance'].screening.videoes_screened.update(viewers = F('viewers') + 1)
#                     else:
#                         old_pma = old_pma_qs[0]
#                         if old_pma.screening_id != kwargs['instance'].screening_id:
#                             old_pma.screening.videoes_screened.update(viewers = F('viewers') - 1)
#                             kwargs['instance'].screening.videoes_screened.update(viewers = F('viewers') + 1)
#                 elif kwargs['signal'] == pre_delete:
#                     kwargs['instance'].screening.videoes_screened.update(viewers = F('viewers') - 1)
#         except Exception:
#             #Catching all to avoid bugs from stopping COCO
#             #Sending exception for immediate attention
#             error_type, value, tracebk = sys.exc_info()
#             mail_body = str(type)+":"+str(value)+"\n"+str(traceback.extract_tb(tracebk))
#             send_mail("Error in update_viewer_handler", mail_body,'server@digitalgreen.org',recipient_list=['rahul@digitalgreen.org'])
#     
#     class Meta:
#         db_table = u'video'
#         unique_together = ("title", "video_production_start_date", "video_production_end_date","village")
# 
#     def get_village(self):
#         return None
#     
#     def __unicode__(self):
#         return  u'%s (%s)' % (self.title, self.village)
# pre_delete.connect(Person.date_of_joining_handler, sender=Video)
# pre_save.connect(Person.date_of_joining_handler, sender=Video)
# m2m_changed.connect(Person.date_of_joining_handler, sender=Video.farmers_shown.through)
# post_save.connect(save_log, sender = Video)
# pre_delete.connect(delete_log, sender = Video)
# 
# class PracticeSector(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=500)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Meta:
#         db_table = u'practice_sector'
# 
# class PracticeSubSector(CocoModel):    
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=500)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Meta:
#         db_table = u'practice_subsector'
# 
# 
# class PracticeTopic(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=500)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Meta:
#         db_table = u'practice_topic'
# 
# 
# class PracticeSubtopic(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=500)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Meta:
#         db_table = u'practice_subtopic'
# 
# class PracticeSubject(CocoModel):
#     id = BigAutoField(primary_key = True)
#     name = models.CharField(max_length=500)
#     
#     def __unicode__(self):
#         return self.name
#     
#     class Meta:
#         db_table = u'practice_subject'
# 
# class Practices(CocoModel):
#     id = BigAutoField(primary_key = True)
#     practice_name = models.CharField(null=True, max_length=200, db_column='PRACTICE_NAME')
#     practice_sector = BigForeignKey(PracticeSector, default=1) 
#     practice_subsector = BigForeignKey(PracticeSubSector, null=True, blank=True)
#     practice_topic = BigForeignKey(PracticeTopic, null=True, blank=True)
#     practice_subtopic = BigForeignKey(PracticeSubtopic, null=True, blank=True)
#     practice_subject = BigForeignKey(PracticeSubject, null=True, blank=True)    
#     class Meta:
#         db_table = u'practices'
#         verbose_name = "Practice"
#         unique_together = ("practice_sector", "practice_subsector", "practice_topic", "practice_subtopic", "practice_subject")
#     
#     def __unicode__(self):
#         practice_sector = '' if self.practice_sector is None else self.practice_sector.name
#         practice_subject = '' if self.practice_subject is None else self.practice_subject.name
#         practice_subsector = '' if self.practice_subsector is None else self.practice_subsector.name
#         practice_topic = '' if self.practice_topic is None else self.practice_topic.name
#         practice_subtopic = '' if self.practice_subtopic is None else self.practice_subtopic.name
#         return "%s, %s, %s, %s, %s" % (practice_sector, practice_subject, practice_subsector, practice_topic, practice_subtopic)
# 
# class Screening(CocoModel):
#     id = BigAutoField(primary_key = True)
#     date = models.DateField(db_column='DATE')
#     start_time = models.TimeField(db_column='START_TIME')
#     end_time = models.TimeField(db_column='END_TIME')
#     location = models.CharField(max_length=200, db_column='LOCATION', blank=True)
#     target_person_attendance = models.IntegerField(null=True, db_column='TARGET_PERSON_ATTENDANCE', blank=True)
#     target_audience_interest = models.IntegerField(null=True, db_column='TARGET_AUDIENCE_INTEREST', blank=True)
#     target_adoptions = models.IntegerField(null=True, db_column='TARGET_ADOPTIONS', blank=True)
#     village = BigForeignKey(Village)
#     fieldofficer = BigForeignKey(FieldOfficer, null=True, blank=True)
#     animator = BigForeignKey(Animator)
#     farmer_groups_targeted = BigManyToManyField(PersonGroups)
#     videoes_screened = BigManyToManyField(Video)
#     farmers_attendance = models.ManyToManyField(Person, through='PersonMeetingAttendance', blank='False', null='False')
#     partner = BigForeignKey(Partners)
#     class Meta:
#         db_table = u'screening'
#         unique_together = ("date", "start_time", "end_time","animator","village")
#      
#     def __unicode__(self):
#         return u'%s %s' % (self.date, self.village)
#     
# pre_save.connect(Person.date_of_joining_handler, sender=Screening)
# m2m_changed.connect(Video.update_viewer_count, sender=Screening.videoes_screened.through)
# post_save.connect(save_log, sender = Screening)
# pre_delete.connect(delete_log, sender = Screening)
#     
# class PersonAdoptPractice(CocoModel):
#     id = BigAutoField(primary_key = True)
#     person = BigForeignKey(Person)
#     video = BigForeignKey(Video)
#     prior_adoption_flag = models.NullBooleanField(null=True, db_column='PRIOR_ADOPTION_FLAG', blank=True)
#     date_of_adoption = models.DateField(db_column='DATE_OF_ADOPTION')
#     quality = models.CharField(max_length=200, db_column='QUALITY', blank=True)
#     quantity = models.IntegerField(null=True, db_column='QUANTITY', blank=True)
#     quantity_unit = models.CharField(max_length=150, db_column='QUANTITY_UNIT', blank=True)
#     time_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
#     partner = BigForeignKey(Partners)
# 
#     def __unicode__(self):
#         return "%s (%s) (%s) (%s)" % (self.person.person_name, self.person.father_name, self.person.village.village_name, self.video.title)
# 
#     def get_village(self):
#         return self.person.village.id
#     def get_partner(self):
#         return self.person.village.block.district.partner.id
#     
#     class Meta:
#         db_table = u'person_adopt_practice'
#         unique_together = ("person", "video", "date_of_adoption")
# post_save.connect(save_log, sender = PersonAdoptPractice)
# pre_delete.connect(delete_log, sender = PersonAdoptPractice)
# 
# class PersonMeetingAttendance(CocoModel):
#     id = BigAutoField(primary_key = True)
#     screening = BigForeignKey(Screening)
#     person = BigForeignKey(Person)
#     interested = models.BooleanField(db_column="INTERESTED", db_index=True)
#     expressed_question = models.CharField(max_length=500,db_column='EXPRESSED_QUESTION', blank=True)
#     expressed_adoption_video = BigForeignKey(Video,related_name='expressed_adoption_video',db_column='EXPRESSED_ADOPTION_VIDEO',null=True, blank=True)
#     
#     def get_village(self):
#         return self.person.village.id
#     def get_partner(self):
#         return self.person.village.block.district.partner.id
#     
#     class Meta:
#         db_table = u'person_meeting_attendance'
#     
#     def __unicode__(self):
#         return  u'%s' % (self.id)
# post_delete.connect(Person.date_of_joining_handler, sender = PersonMeetingAttendance)
# pre_delete.connect(Video.update_viewer_count, sender = PersonMeetingAttendance)
# pre_save.connect(Person.date_of_joining_handler, sender = PersonMeetingAttendance)
# pre_save.connect(Video.update_viewer_count, sender = PersonMeetingAttendance)
# post_save.connect(save_log, sender = PersonMeetingAttendance)
# pre_delete.connect(delete_log, sender = PersonMeetingAttendance)
# 
# class Equipment(CocoModel):
#     id = BigAutoField(primary_key = True)
#     equipment_type = models.IntegerField(choices=EQUIPMENT, db_column='EQUIPMENT_TYPE')
#     other_equipment = models.CharField("Specify the equipment if 'Other' equipment type has been selected ", max_length=300, db_column='OTHER_EQUIPMENT', null = True, blank=True)
#     invoice_no = models.CharField(max_length=300, db_column='INVOICE_NO')
#     model_no = models.CharField("Make / Model No ", max_length=300, db_column='MODEL_NO', blank=True)
#     serial_no = models.CharField(max_length=300, db_column='SERIAL_NO', blank=True)
#     cost = models.FloatField(null=True, db_column='COST', blank=True)
#     purpose = models.IntegerField(choices=EQUIPMENT_PURPOSE, db_column='purpose', null=True, blank=True)
#     additional_accessories = models.CharField("Additional Accessories Supplied", max_length=500, blank=True)
#     is_reserve = models.BooleanField("Is the equipment in Reserve?")
#     procurement_date = models.DateField(null=True, db_column='PROCUREMENT_DATE', blank=True)
#     transfer_date = models.DateField("Transfer from DG to Partner date", null=True, blank=True)
#     installation_date = models.DateField("Field Installation Date", null=True, blank=True)
#     warranty_expiration_date = models.DateField(null=True, db_column='WARRANTY_EXPIRATION_DATE', blank=True)
#     village = BigForeignKey(Village, null=True, blank=True)
#     equipmentholder = BigForeignKey(EquipmentHolder,null=True,blank=True)
#     remarks = models.TextField(blank=True)    
# 
#     class Meta:
#         db_table = u'equipment_id'
# 
# class UserPermission(CocoModel):
#     username = models.ForeignKey(User)
#     role = models.CharField(max_length=1,choices=ROLE)
#     region_operated = BigForeignKey(Region, null=True, blank=True)
#     district_operated = BigForeignKey(District, null=True, blank=True)
# 
# class Target(CocoModel):
#     id = BigAutoField(primary_key = True)
#     district = BigForeignKey(District)
#     month_year = models.DateField("Month & Year")
# 
#     clusters_identification = models.IntegerField("Villages Identification", null=True, blank=True)
#     dg_concept_sharing = models.IntegerField("DG Concept Sharing", null=True, blank=True)
#     csp_identification = models.IntegerField("CSP Identified", null=True, blank=True)
#     dissemination_set_deployment = models.IntegerField(null=True, blank=True)
#     village_operationalization = models.IntegerField(null=True, blank=True)
#     video_uploading = models.IntegerField(null=True, blank=True)
#     video_production = models.IntegerField(null=True, blank=True)
#     storyboard_preparation = models.IntegerField(null=True, blank=True)
#     video_shooting = models.IntegerField(null=True, blank=True)
#     video_editing = models.IntegerField(null=True, blank=True)
#     video_quality_checking = models.IntegerField(null=True, blank=True)
#     disseminations = models.IntegerField(null=True, blank=True)
#     avg_attendance_per_dissemination = models.IntegerField("Average Attendance per Dissemination", null=True, blank=True)
#     exp_interest_per_dissemination = models.IntegerField("Expressed Interest per Dissemination", null=True, blank=True)
#     adoption_per_dissemination = models.IntegerField("Adoption per Dissemination", null=True, blank=True)
#     crp_training = models.IntegerField("CRP Training", null=True, blank=True)
#     crp_refresher_training = models.IntegerField("CRP Refresher Training", null=True, blank=True)
#     csp_training = models.IntegerField("CSP Training", null=True, blank=True)
#     csp_refresher_training = models.IntegerField("CSP Refresher Training", null=True, blank=True)
#     editor_training = models.IntegerField(null=True, blank=True)
#     editor_refresher_training = models.IntegerField(null=True, blank=True)
#     villages_certification = models.IntegerField(null=True, blank=True)
#     what_went_well =  models.TextField("What went well and why?", blank=True)
#     what_not_went_well =  models.TextField("What did NOT go well and why?", blank=True)
#     challenges =  models.TextField(blank=True)
#     support_requested =  models.TextField(blank=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     
#     class Meta:
#         unique_together = ("district","month_year")
#         
# class CocoUser(CocoModel):
#     user = models.OneToOneField(User)
#     partner = BigForeignKey(Partners)
#     villages = BigManyToManyField(Village)
#     
#     def get_villages(self):
#         return self.villages.all()
# 
# 
# class Rule(CocoModel):
#     name = models.CharField(max_length=100);
#     error_msg = models.CharField(max_length=500);
#     description = models.TextField(blank=True)
#     
#     def __unicode__(self):
#         return u'%s' % (self.name)
# 
# class Error(CocoModel):
#     rule = models.ForeignKey(Rule)
#     district = BigForeignKey(District)
#     content_type1 = models.ForeignKey(ContentType, related_name = 'content_type1')
#     object_id1 = PositiveBigIntegerField()
#     content_object1 = generic.GenericForeignKey('content_type1', 'object_id1')
#     content_type2 = models.ForeignKey(ContentType, related_name = 'content_type2', null=True)
#     object_id2 = PositiveBigIntegerField(null=True)
#     content_object2 = generic.GenericForeignKey('content_type2', 'object_id2')
#     notanerror = models.BooleanField(default=False)
#     
#     class Meta:
#         unique_together = ("rule","content_type1","object_id1","content_type2","object_id2")
#         
#     def __unicode__(self):
#         return u'%s; %s; %s' % (self.rule, self.content_object1, self.content_object2)
#     
# class VillagePrecalculation(CocoModel):
#     village = BigForeignKey(Village)
#     date = models.DateField()
#     total_adopted_attendees = models.PositiveIntegerField(default=0)
#     total_active_attendees = models.PositiveIntegerField(default=0)
#     total_adoption_by_active = models.PositiveIntegerField(default=0)
#     
#     class Meta:
#         unique_together = ("village", "date")
#         db_table = u'village_precalculation'
#         
# 
# class TrainingAnimatorsTrained(models.Model):
#     id = BigAutoField(primary_key = True)
#     training = BigForeignKey(Training, db_column='training_id')
#     animator = BigForeignKey(Animator, db_column='animator_id')
#     class Meta:
#         db_table = u'training_animators_trained'
# 
# class GroupsTargetedInScreening(models.Model):
#     id = BigAutoField(primary_key = True)
#     screening = BigForeignKey(Screening, db_column='screening_id')
#     persongroups = BigForeignKey(PersonGroups, db_column='persongroups_id')
#     class Meta:
#         db_table = u'screening_farmer_groups_targeted'
# 
# class VideosScreenedInScreening(models.Model):  
#     id = BigAutoField(primary_key = True)
#     screening = BigForeignKey(Screening, db_column='screening_id')
#     video = BigForeignKey(Video, db_column='video_id')
#     class Meta:
#         db_table = u'screening_videoes_screened'
# 
# class PersonShownInVideo(models.Model):
#     id = BigAutoField(primary_key = True)
#     video = BigForeignKey(Video, db_column='video_id')
#     person = BigForeignKey(Person, db_column='person_id')
#     class Meta:
#         db_table = u'video_farmers_shown'
#         
#===============================================================================
