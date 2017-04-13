from django.db import models
from coco.base_models import CocoModel
from django.db.models.signals import post_save, pre_delete
from training.log.training_log import enter_to_log


class Partner(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True, db_index=True)
    partner_name = models.CharField(max_length=100, help_text="Short Name of Partner. It will be display on Analytics")
    full_partner_name = models.CharField(max_length=200, default='', blank=True)
    date_of_association = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.partner_name

post_save.connect(enter_to_log,sender=Partner)
pre_delete.connect(enter_to_log,sender=Partner)

class Project(CocoModel):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, unique=True, help_text="Short Name of Project. It will be display on Analytics")
    project_description = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    associate_partner = models.ManyToManyField(Partner)

    def __unicode__(self):
        return self.project_name
