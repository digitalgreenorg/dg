from django.db import models
from django.db.models.signals import pre_delete, post_save

from coco.data_log import delete_log, save_log
from coco.base_models import CocoModel, DAY_CHOICES, GENDER_CHOICES
from farmerbook.managers import FarmerbookManager
from geographies.models import District, Village
from programs.models import Partner

class Animator(CocoModel):
    id = models.AutoField(primary_key = True)
    old_coco_id = models.BigIntegerField(editable=False, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=100, blank=True)
    partner = models.ForeignKey(Partner)
    district = models.ForeignKey(District, null=True, blank=True)
    assigned_villages = models.ManyToManyField(Village, related_name='assigned_villages', through='AnimatorAssignedVillage', null=True, blank=True)
    total_adoptions = models.PositiveIntegerField(default=0, blank=True, editable=False) 

    class Meta:
        unique_together = ("name", "gender", "partner", "district")

    def get_village(self):
        return None

    def get_partner(self):
        return self.partner.id

    def __unicode__(self):
        return  u'%s (%s)' % (self.name, self.district)

post_save.connect(save_log, sender=Animator)
pre_delete.connect(delete_log, sender=Animator)


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
    age = models.IntegerField(max_length=3, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = models.CharField(max_length=100, blank=True)
    village = models.ForeignKey(Village)
    group = models.ForeignKey(PersonGroup, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    image_exists = models.BooleanField(default=False)
    partner = models.ForeignKey(Partner)
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