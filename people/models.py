from django.db import models
from django.db.models.signals import pre_delete, post_save

from coco.data_log import delete_log, save_log
from coco.base_models import CocoModel, DAY_CHOICES, GENDER_CHOICES, TYPE_OF_ROLE
from farmerbook.managers import FarmerbookManager
from geographies.models import *
from coco.base_models import ACTIVITY_CHOICES
from programs.models import Partner
from training.log.training_log import enter_to_log


class Animator(CocoModel):
    id = models.AutoField(primary_key = True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=100, blank=True)
    partner = models.ForeignKey(Partner)
    district = models.ForeignKey(District, null=True, blank=True)
    assigned_villages = models.ManyToManyField(Village, related_name='assigned_villages', through='AnimatorAssignedVillage', blank=True)
    total_adoptions = models.PositiveIntegerField(default=0, blank=True, editable=False)
    role = models.IntegerField(default = 0, choices = TYPE_OF_ROLE)

    class Meta:
        unique_together = ("name", "gender", "partner", "district", "role", "phone_no")

    def get_village(self):
        return None

    def get_partner(self):
        return self.partner.id

    def get_district(self):
        return self.district.id

    def __unicode__(self):
        return  u'%s (%s)' % (self.name, self.district)

post_save.connect(save_log, sender=Animator)
post_save.connect(enter_to_log, sender=Animator)
pre_delete.connect(delete_log, sender=Animator)
pre_delete.connect(enter_to_log, sender=Animator)


class AnimatorAssignedVillage(CocoModel):
    id = models.AutoField(primary_key=True)
    animator = models.ForeignKey(Animator)
    village = models.ForeignKey(Village)
    start_date = models.DateField(null=True, blank=True)


class PersonGroup(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    group_name = models.CharField(max_length=100)
    village = models.ForeignKey(Village)
    partner = models.ForeignKey(Partner)

    class Meta:
        verbose_name = "Person group"
        unique_together = ("group_name", "village")

    def __unicode__(self):
        return  u'%s (%s)' % (self.group_name, self.village)
post_save.connect(save_log, sender=PersonGroup)
pre_delete.connect(delete_log, sender=PersonGroup)


class Person(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    person_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(999)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=100, blank=True)
    village = models.ForeignKey(Village)
    group = models.ForeignKey(PersonGroup, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    image_exists = models.BooleanField(default=False)
    partner = models.ForeignKey(Partner)
    is_modelfarmer = models.BooleanField(default=False)
    objects = models.Manager() #The default manager
    farmerbook_objects = FarmerbookManager() #The manager for farmerbook


    class Meta:
        unique_together = ("person_name", "father_name", "village")

    def __unicode__(self):
        display = "%s" % (self.person_name)
        display += " (%s)" % self.father_name if self.father_name.strip()!="" else ""
        display += " (%s)" % self.group.group_name if self.group is not None else ""
        display += " (%s)" % self.village.village_name
        return  display
post_save.connect(save_log, sender=Person)
pre_delete.connect(delete_log, sender=Person)


class JSLPS_Animator(CocoModel):
    id = models.AutoField(primary_key=True)
    animator_code = models.CharField(max_length=100)
    animator = models.ForeignKey(Animator, null=True, blank=True)
    assigned_villages = models.ManyToManyField(JSLPS_Village, related_name='jslps_assigned_villages', through='JSLPS_AnimatorAssignedVillage', blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS Animator"
        verbose_name_plural = "JSLPS Animator"

    def __unicode__(self):
        return self.animator_code


class JSLPS_AnimatorAssignedVillage(CocoModel):
    id = models.AutoField(primary_key=True)
    animator = models.ForeignKey(JSLPS_Animator)
    village = models.ForeignKey(JSLPS_Village)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS AnimatorAssignedVillage"
        verbose_name_plural = "JSLPS AnimatorAssignedVillage"


class JSLPS_Persongroup(CocoModel):
    id = models.AutoField(primary_key=True)
    group_code = models.CharField(max_length=100)
    group = models.ForeignKey(PersonGroup, null=True, blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS Persongroup"
        verbose_name_plural = "JSLPS Persongroup"


class JSLPS_Person(CocoModel):
    id = models.AutoField(primary_key=True)
    person_code = models.CharField(max_length=100)
    person = models.ForeignKey(Person, null=True, blank=True)
    group = models.ForeignKey(JSLPS_Persongroup, null=True, blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "JSLPS Person"
        verbose_name_plural = "JSLPS Person"


class AP_Animator(CocoModel):
    animator_code = models.CharField(max_length=100)
    animator = models.ForeignKey(Animator, null=True, blank=True)
    assigned_villages = models.ManyToManyField(AP_Village, related_name='ap_assigned_villages', through='AP_AnimatorAssignedVillage', blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "AP Animator"
        verbose_name_plural = "AP Animator"

    def __unicode__(self):
        return self.animator_code


class AP_AnimatorAssignedVillage(CocoModel):
    animator = models.ForeignKey(AP_Animator)
    village = models.ForeignKey(AP_Village)

    class Meta:
        verbose_name = "AP AnimatorAssignedVillage"
        verbose_name_plural = "AP AnimatorAssignedVillage"


class AP_Person(CocoModel):
    person_code = models.CharField(max_length=100)
    person = models.ForeignKey(Person, null=True, blank=True)
    habitation = models.ForeignKey(AP_Habitation, null=True, blank=True)

    class Meta:
        verbose_name = "AP Person"
        verbose_name_plural = "AP Person"

