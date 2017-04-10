from django.db import models
from coco.base_models import CocoModel


class Partner(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField(editable=False, null=True, db_index=True)
    partner_name = models.CharField(max_length=100)
    full_partner_name = models.CharField(max_length=200, default='', blank=True)
    date_of_association = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.partner_name


class Project(CocoModel):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, unique=True)
    project_description = models.CharField(max_length=200, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    associate_partner = models.ManyToManyField(Partner, blank=True)
    
    def __unicode__(self):
        return self.project_name

