from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save

from dashboard.base_models import CocoModel
from dashboard.data_log import delete_log, save_log
from dashboard.models import VillageFarmerbookManager
from libs.geocoder import Geocoder
from programs.models import Partner

import logging


class Country(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    country_name = models.CharField(max_length=100, unique='True')
    start_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "countries"

    def __unicode__(self):
        return self.country_name


class Region(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    region_name = models.CharField(max_length=100, unique='True')
    start_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.region_name


class State(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    state_name = models.CharField(max_length=100, unique='True')
    region = models.ForeignKey(Region)
    country = models.ForeignKey(Country)
    start_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.state_name


class District(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    district_name = models.CharField(max_length=100, unique='True')
    start_date = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State)
    partner = models.ForeignKey(Partner)
    latitude = models.DecimalField(max_digits=31, decimal_places=28, null=True, blank=True,
                                   validators=[MaxValueValidator(90), MinValueValidator(-90)])
    longitude = models.DecimalField(max_digits=32, decimal_places=28, null=True, blank=True,
                                    validators=[MaxValueValidator(180), MinValueValidator(-180)])

    def __unicode__(self):
        return self.district_name

    def clean(self):
        logger = logging.getLogger('dashboard')
        if(self.latitude is None or self.longitude is None):
            geocoder = Geocoder()
            address = u"%s,%s,%s" % (self.district_name, self.state.state_name, self.state.country.country_name)
            if (geocoder.convert(address)):
                try:
                    (self.latitude, self.longitude) = geocoder.getLatLng()
                    logger.info("%s: Lat Long Added" % self.district_name)
                except:
                    logger.error("Geocodes not found for %s, %s" % (self.district_name, self.state.state_name))


class Block(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    block_name = models.CharField(max_length=100, unique='True')
    start_date = models.DateField(null=True, blank=True)
    district = models.ForeignKey(District)

    def __unicode__(self):
        return self.block_name


class Village(CocoModel):
    id = models.AutoField(primary_key=True)
    old_coco_id = models.BigIntegerField()
    village_name = models.CharField(max_length=100)
    block = models.ForeignKey(Block)
    no_of_households = models.IntegerField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)
    road_connectivity = models.CharField(max_length=100, blank=True)
    control = models.NullBooleanField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    latitude = models.CharField(max_length=25, null=True, blank=True)
    longitude = models.CharField(max_length=25, null=True, blank=True)
    grade = models.CharField(max_length=1, null=True, blank=True)
    objects = models.Manager() #The default manager
    farmerbook_village_objects = VillageFarmerbookManager() #The manager for farmerbook

    class Meta:
        unique_together = ("village_name","block")

    def get_village(self):
        return self.id
    def get_partner(self):
        return self.block.district.partner.id

    def __unicode__(self):
        return self.village_name
post_save.connect(save_log, sender = Village)
pre_delete.connect(delete_log, sender = Village)

