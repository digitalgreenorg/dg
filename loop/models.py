# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from loop.utils.send_log.loop_data_log import save_log  # , delete_log
from loop.utils.send_log.loop_admin_log import save_admin_log  # , delete_log
from smart_selects.db_fields import ChainedForeignKey
from constants.constants import *

ROLE_CHOICE = ((ROLE_CHOICE_ADMIN, "Admin"), (ROLE_CHOICE_AGGREGATOR, "Aggregator"), (ROLE_CHOICE_TESTING, "Testing"))
MODEL_CHOICE = ((1, "Direct Sell"), (2, "Aggregate"))
DISCOUNT_CRITERIA = ((DISCOUNT_CRITERIA_VOLUME, "Volume"), (DISCOUNT_CRITERIA_AMOUNT, "Amount"))
MODEL_TYPES = (
(MODEL_TYPES_DIRECT, "Direct"), (MODEL_TYPES_TAX_BASED, "Tax Based"), (MODEL_TYPES_SLAB_BASED, "Slab Based"),
(MODEL_TYPES_DAILY_PAY, "Daily Pay"))
CALL_TYPES = ((0, "Incoming"), (1, "Outgoing"))
CALL_STATUS = ((0, "Pending"), (1, "Resolved"), (2, "Declined"))
EXPERT_STATUS = ((0, "Inactive"), (1, "Active"))
BROADCAST_STATUS = ((0, "Pending"), (1, "Done"), (2, "DND-Failed"), (3, "Declined"))
MANDI_CATEGORY = ((0, "Wholesale Market"), (1, "Retail Market"), (2, "Individual Entity"))
PERSON_TYPE = ((0, 'Farmer'), (1, 'Transporter'))
SMS_STATUS = ((0, 'Fail'), (1, 'Success'))
SMS_STATE = {'N':(0,'None'), 'S':(1,'SMS initiated'), 'F':(2,'SMS fired'), 'D':(3,'SMS delivered'), 'U':(4,'SMS undelivered'), 'P':(5,'pending en route'), 'I':(6,'invalid no.'), 'E':(7,'expired'), '?':(8,'pushed to network en route'), 'B':(9,'DND block')}

class LoopModel(models.Model):
    user_created = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created", editable=False, null=True, blank=True)
    time_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_related_modified", editable=False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    notation = models.CharField(max_length=3, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Country(LoopModel):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=50)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.country_name

    class Meta:
        unique_together = ("country_name",)


class State(LoopModel):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)
    is_visible = models.BooleanField(default=True)
    state_name_en = models.CharField(max_length=100)
    helpline_number = models.CharField(max_length=14, null=False, blank=False, default="0")
    crop_add = models.BooleanField(default=False)
    phone_digit = models.CharField(default=10, max_length=2, blank=True, null=True)
    phone_start = models.CharField(default='7,8,9', max_length=15, blank=True, null=True)
    aggregation_state = models.BooleanField(default=True)
    server_sms = models.BooleanField(default=False)

    def __unicode__(self):
        return self.state_name_en

    class Meta:
        unique_together = ("state_name", "country")


post_save.connect(save_log, sender=State)
pre_delete.connect(save_log, sender=State)


class District(LoopModel):
    id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=50)
    state = models.ForeignKey(State)
    is_visible = models.BooleanField(default=True)
    district_name_en = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s (%s)" % (self.district_name_en, self.state.state_name_en)

    class Meta:
        unique_together = ("district_name", "state")


class Block(LoopModel):
    id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=50)
    district = models.ForeignKey(District)
    is_visible = models.BooleanField(default=True)
    block_name_en = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s (%s)" % (self.block_name_en, self.district.district_name_en)

    class Meta:
        unique_together = ("block_name", "district")


post_save.connect(save_admin_log, sender=Block)
pre_delete.connect(save_admin_log, sender=Block)


class Village(LoopModel):
    id = models.AutoField(primary_key=True)
    village_name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    block = models.ForeignKey(Block)
    is_visible = models.BooleanField(default=True)
    village_name_en = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s (%s)" % (self.village_name_en, self.block.block_name_en)

    class Meta:
        unique_together = ("village_name", "block")


post_save.connect(save_log, sender=Village)
pre_delete.connect(save_log, sender=Village)
post_save.connect(save_admin_log, sender=Village)
pre_delete.connect(save_admin_log, sender=Village)


class MandiType(LoopModel):
    id = models.AutoField(primary_key=True)
    mandi_type_name = models.CharField(max_length=100)
    mandi_category = models.IntegerField(choices=MANDI_CATEGORY, default=0)
    type_description = models.CharField(max_length=300, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.mandi_type_name, self.mandi_category)

    class Meta:
        unique_together = ("mandi_type_name", "mandi_category")


class Mandi(LoopModel):
    id = models.AutoField(primary_key=True)
    mandi_name = models.CharField(max_length=90)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    district = models.ForeignKey(District)
    is_visible = models.BooleanField(default=True)
    mandi_name_en = models.CharField(max_length=100)
    mandi_type = models.ForeignKey(MandiType, default=None, null=True)


    def __unicode__(self):
        return "%s (%s)" % (self.mandi_name_en, self.district.district_name_en)

    class Meta:
        unique_together = ("mandi_name", "district",)


post_save.connect(save_log, sender=Mandi)
pre_delete.connect(save_log, sender=Mandi)
post_save.connect(save_admin_log, sender=Mandi)
pre_delete.connect(save_admin_log, sender=Mandi)


class Partner(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_visible = models.BooleanField(verbose_name="Is Active", default=True)
    start_date = models.DateField()
    helpline_number = models.CharField(max_length=14, null=False, blank=False, default="0")

    def __unicode__(self):
        return "%s" % (self.name)


class LoopUser(LoopModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="loop_user")
    name = models.CharField(max_length=100, default="default")
    role = models.IntegerField(choices=ROLE_CHOICE)
    assigned_villages = models.ManyToManyField(
        Village, related_name="assigned_villages", through='LoopUserAssignedVillage', blank=True)
    assigned_mandis = models.ManyToManyField(
        Mandi, related_name="assigned_mandis", through='LoopUserAssignedMandi', blank=True)
    mode = models.IntegerField(choices=MODEL_CHOICE, default=1)
    phone_number = models.CharField(
        max_length=14, null=False, blank=False, default="0")
    village = models.ForeignKey(Village, default=None, null=True)
    name_en = models.CharField(max_length=100)
    preferred_language = models.ForeignKey(Language, null=True)
    days_count = models.IntegerField(default=3)
    is_visible = models.BooleanField(verbose_name="Is Active", default=True)
    farmer_phone_mandatory = models.BooleanField(default=True)
    registration = models.CharField(max_length=200, default="", null=True, blank=True)
    show_farmer_share = models.BooleanField(default=True)
    percent_farmer_share = models.FloatField(default=0.0)
    partner = models.ForeignKey(Partner, default=None, null=True, blank=True)
    version = models.CharField(max_length=10, blank=True, null=True, default="0")

    def __unicode__(self):
        return """%s (%s)""" % (self.name_en, self.phone_number)

    def get_villages(self):
        return self.assigned_villages.all()

    def get_mandis(self):
        return self.assigned_mandis.all()

    def __user__(self):
        return "%s" % self.user.id


post_save.connect(save_log, sender=LoopUser)
pre_delete.connect(save_log, sender=LoopUser)
post_save.connect(save_admin_log, sender=LoopUser)
pre_delete.connect(save_admin_log, sender=LoopUser)


class LoopUserAssignedMandi(LoopModel):
    id = models.AutoField(primary_key=True)
    loop_user = models.ForeignKey(LoopUser)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)


post_save.connect(save_log, sender=LoopUserAssignedMandi)
pre_delete.connect(save_log, sender=LoopUserAssignedMandi)
post_save.connect(save_admin_log, sender=LoopUserAssignedMandi)
pre_delete.connect(save_admin_log, sender=LoopUserAssignedMandi)


class LoopUserAssignedVillage(LoopModel):
    id = models.AutoField(primary_key=True)
    loop_user = models.ForeignKey(LoopUser)
    village = models.ForeignKey(Village)
    is_visible = models.BooleanField(default=True)


post_save.connect(save_log, sender=LoopUserAssignedVillage)
pre_delete.connect(save_log, sender=LoopUserAssignedVillage)
post_save.connect(save_admin_log, sender=LoopUserAssignedVillage)
pre_delete.connect(save_admin_log, sender=LoopUserAssignedVillage)


class AdminUser(LoopModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="admin_user")
    name = models.CharField(max_length=100, default="default")
    assigned_districts = models.ManyToManyField(
        District, through='AdminAssignedDistrict', blank=True)
    assigned_loopusers = models.ManyToManyField(LoopUser, through='AdminAssignedLoopUser')
    phone_number = models.CharField(
        max_length=14, null=False, blank=False, default="0")
    name_en = models.CharField(max_length=100)
    preferred_language = models.ForeignKey(Language, null=True)
    is_visible = models.BooleanField(default=True)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name

    def get_districts(self):
        return self.assigned_districts.all()

    def get_loopusers(self):
        return self.assigned_loopusers.all()

    def __user__(self):
        return "%s" % self.user.id


post_save.connect(save_admin_log, sender=AdminUser)
pre_delete.connect(save_admin_log, sender=AdminUser)


class AdminAssignedLoopUser(LoopModel):
    id = models.AutoField(primary_key=True)
    admin_user = models.ForeignKey(AdminUser)
    loop_user = models.ForeignKey(LoopUser)
    is_visible = models.BooleanField(default=True)


post_save.connect(save_admin_log, sender=AdminAssignedLoopUser)
pre_delete.connect(save_admin_log, sender=AdminAssignedLoopUser)


class AdminAssignedDistrict(LoopModel):
    id = models.AutoField(primary_key=True)
    admin_user = models.ForeignKey(AdminUser)
    district = models.ForeignKey(District)
    aggregation_switch = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)


post_save.connect(save_admin_log, sender=AdminAssignedDistrict)
pre_delete.connect(save_admin_log, sender=AdminAssignedDistrict)


class Gaddidar(LoopModel):
    id = models.AutoField(primary_key=True)
    gaddidar_name = models.CharField(max_length=100)
    gaddidar_phone = models.CharField(max_length=13)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)
    gaddidar_name_en = models.CharField(max_length=100)
    discount_criteria = models.IntegerField(choices=DISCOUNT_CRITERIA, default=0)
    commission = models.FloatField("Discount", default=1.0)
    is_prime = models.BooleanField(default=False)

    def __unicode__(self):
        return self.gaddidar_name_en

    class Meta:
        unique_together = ("gaddidar_phone", "gaddidar_name", "mandi")


post_save.connect(save_log, sender=Gaddidar)
pre_delete.connect(save_log, sender=Gaddidar)
post_save.connect(save_admin_log, sender=Gaddidar)
pre_delete.connect(save_admin_log, sender=Gaddidar)


class Farmer(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)  # M/F
    phone = models.CharField(max_length=13)
    image_path = models.CharField(
        max_length=500, default=None, null=True, blank=True)
    village = models.ForeignKey(Village)
    is_visible = models.BooleanField(default=True)
    correct_phone_date = models.DateField(default=None, auto_now=False, null=True)
    registration_sms = models.BooleanField(default=False)
    registration_sms_id = models.CharField(max_length=15, null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.village.village_name_en)

    def __village__(self):
        return "%s" % (self.village.village_name_en)

    class Meta:
        unique_together = ("phone", "name", "village")


post_save.connect(save_log, sender=Farmer)
pre_delete.connect(save_log, sender=Farmer)


class Crop(LoopModel):
    id = models.AutoField(primary_key=True)
    image_path = models.CharField(
        max_length=500, default=None, null=True, blank=True)
    crop_name = models.CharField(max_length=30, null=False, blank=False)
    measuring_unit = models.CharField(max_length=20, default="kg")
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.crop_name

    class Meta:
        unique_together = ("crop_name",)


post_save.connect(save_log, sender=Crop)
pre_delete.connect(save_log, sender=Crop)
post_save.connect(save_admin_log, sender=Crop)
pre_delete.connect(save_admin_log, sender=Crop)
# ############Crop name in multiple languages###############

class CropLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language)
    crop = models.ForeignKey(Crop, related_name="crops")
    crop_name = models.CharField(max_length=30)
    measuring_unit = models.CharField(max_length=20, default="kg")
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.crop_name

    def __crop__(self):
        return "%s" % (self.crop.crop_name)

    class Meta:
        unique_together = ("crop", "language",)


post_save.connect(save_log, sender=CropLanguage)
pre_delete.connect(save_log, sender=CropLanguage)
post_save.connect(save_admin_log, sender=CropLanguage)
pre_delete.connect(save_admin_log, sender=CropLanguage)


class Transporter(LoopModel):
    id = models.AutoField(primary_key=True)
    transporter_name = models.CharField(max_length=90)
    transporter_phone = models.CharField(max_length=13)
    block = models.ForeignKey(Block)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.transporter_name)

    def __block__(self):
        return "%s" % (self.block.block_name_en)

    class Meta:
        unique_together = ("transporter_name", "transporter_phone",)


post_save.connect(save_log, sender=Transporter)
pre_delete.connect(save_log, sender=Transporter)


class Vehicle(LoopModel):
    id = models.AutoField(primary_key=True)
    vehicle_name = models.CharField(max_length=30, blank=False, null=False)
    is_visible = models.BooleanField(default=True)
    vehicle_name_en = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.vehicle_name

    class Meta:
        unique_together = ("vehicle_name",)


post_save.connect(save_log, sender=Vehicle)
pre_delete.connect(save_log, sender=Vehicle)
post_save.connect(save_admin_log, sender=Vehicle)
pre_delete.connect(save_admin_log, sender=Vehicle)


class VehicleLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language)
    vehicle = models.ForeignKey(Vehicle, related_name="vehicles")
    vehicle_name = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.vehicle_name

    def __vehicle__(self):
        return "%s" % (self.vehicle.vehicle_name)

    class Meta:
        unique_together = ("vehicle", "language",)


post_save.connect(save_log, sender=VehicleLanguage)
pre_delete.connect(save_log, sender=VehicleLanguage)
post_save.connect(save_admin_log, sender=VehicleLanguage)
pre_delete.connect(save_admin_log, sender=VehicleLanguage)


class TransportationVehicle(LoopModel):
    id = models.AutoField(primary_key=True)
    transporter = models.ForeignKey(Transporter)
    vehicle = models.ForeignKey(Vehicle)
    vehicle_number = models.CharField(max_length=20)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.transporter.transporter_name, self.vehicle.vehicle_name, self.vehicle_number)

    def __transporter__(self):
        return "%s" % (self.transporter.transporter_name)

    def __vehicle__(self):
        return "%s" % (self.vehicle.vehicle_name)

    class Meta:
        unique_together = ("transporter", "vehicle", "vehicle_number",)


post_save.connect(save_log, sender=TransportationVehicle)
pre_delete.connect(save_log, sender=TransportationVehicle)


class DayTransportation(LoopModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False)
    transportation_vehicle = models.ForeignKey(TransportationVehicle)
    transportation_cost = models.FloatField()
    farmer_share = models.FloatField(default=0.0)
    other_cost = models.FloatField(default=0.0)
    vrp_fees = models.FloatField(default=0.0)
    farmer_share_comment = models.CharField(max_length=200, null=True, blank=True)
    transportation_cost_comment = models.CharField(max_length=200, null=True, blank=True)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)
    timestamp = models.CharField(max_length=25)
    payment_sms = models.IntegerField(
        default=0)  #0-None, 1-SMS initiated, 2-SMS fired, 3-SMS delivered, 4-SMS undelivered, 5-pending en route, 6-invalid no., 7-expired, 8-pushed to network en route, 9-DND block
    payment_sms_id = models.CharField(max_length=15, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (
        LoopUser.objects.get(user=self.user_created).name_en, self.transportation_vehicle.transporter.transporter_name,
        self.transportation_vehicle.vehicle.vehicle_name)

    def __aggregator__(self):
        return "%s" % (LoopUser.objects.get(user=self.user_created).name_en)

    def __transporter__(self):
        return "%s" % (self.transportation_vehicle.transporter.transporter_name)

    def __vehicle__(self):
        return "%s (%s)" % (
        self.transportation_vehicle.vehicle.vehicle_name, self.transportation_vehicle.vehicle_number)

    def __mandi__(self):
        return "%s" % (self.mandi.mandi_name)

    def __transporter_phone__(self):
        return "%s" % (self.validate_phone_number(self.transportation_vehicle.transporter.block.district.state,
                                                  self.transportation_vehicle.transporter.transporter_phone))

    def validate_phone_number(self, state, phone):
        if len(phone) == int(state.phone_digit):
            return phone
        return ""

    class Meta:
        unique_together = ("date", "user_created", "timestamp")


post_save.connect(save_log, sender=DayTransportation)
pre_delete.connect(save_log, sender=DayTransportation)


class CombinedTransaction(LoopModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=False)
    farmer = models.ForeignKey(Farmer)
    crop = models.ForeignKey(Crop)
    mandi = models.ForeignKey(Mandi)
    gaddidar = models.ForeignKey(Gaddidar, null=True, default=True)
    quantity = models.FloatField()
    price = models.FloatField()
    status = models.IntegerField()
    amount = models.FloatField()
    timestamp = models.CharField(max_length=25)
    is_visible = models.BooleanField(default=True)
    payment_date = models.DateField(auto_now=False, null=True, blank=True)
    payment_sms = models.IntegerField(
        default=0)  #0-None, 1-SMS initiated form DG, 2-SMS fired from DG, 3-SMS delivered, 4-SMS undelivered, 5-pending en route, 6-invalid no., 7-expired, 8-pushed to network en route, 9-DND block
    payment_sms_id = models.CharField(max_length=15, null=True, blank=True)

    def __unicode__(self):
        return "%s (%s) (%s) (%s)" % (
            self.farmer.name, self.crop.crop_name, self.mandi.mandi_name_en,
            LoopUser.objects.get(user=self.user_created).name_en)

    def __aggregator__(self):
        return "%s" % (LoopUser.objects.get(user=self.user_created).name_en)

    def __farmer__(self):
        return "%s" % (self.farmer.name)

    def __crop__(self):
        return "%s" % (self.crop.crop_name)

    def __mandi__(self):
        return "%s" % (self.mandi.mandi_name_en)

    def __gaddidar__(self):
        return "%s" % (self.gaddidar.gaddidar_name_en)

    def __farmer_phone__(self):
        return "%s" % (self.validate_phone_number(self.farmer.village.block.district.state, self.farmer.phone))

    def validate_phone_number(self, state, phone):
        if len(phone) == int(state.phone_digit):
            return phone
        return ""

    class Meta:
        unique_together = ("date", "user_created", "timestamp")


post_save.connect(save_log, sender=CombinedTransaction)
pre_delete.connect(save_log, sender=CombinedTransaction)


class GaddidarCommission(LoopModel):
    mandi = models.ForeignKey(Mandi)
    gaddidar = ChainedForeignKey(Gaddidar, chained_field="mandi", chained_model_field="mandi")
    start_date = models.DateField(auto_now=False)
    discount_percent = models.FloatField(verbose_name="Discount", validators=[MinValueValidator(0.0),
                                                                              MaxValueValidator(1.0)], default=0.0)

    def __unicode__(self):
        return "%s (%s)" % (
            self.gaddidar.gaddidar_name, self.mandi.mandi_name)

    class Meta:
        unique_together = ("start_date", "gaddidar", "mandi")


post_save.connect(save_log, sender=GaddidarCommission)
pre_delete.connect(save_log, sender=GaddidarCommission)
post_save.connect(save_admin_log, sender=GaddidarCommission)
pre_delete.connect(save_admin_log, sender=GaddidarCommission)


class GaddidarShareOutliers(LoopModel):
    mandi = ChainedForeignKey(Mandi, chained_field="aggregator", chained_model_field="assigned_mandis")
    gaddidar = ChainedForeignKey(Gaddidar, chained_field="mandi", chained_model_field="mandi")
    aggregator = models.ForeignKey(LoopUser)
    date = models.DateField(auto_now=False)
    amount = models.FloatField()
    comment = models.CharField(max_length=200, null=True, blank=True)
    # loop_user = models.ForeignKey(LoopUser,null=True,related_name="loop_user")

    def __unicode__(self):
        return "%s (%s)" % (
            self.gaddidar.gaddidar_name_en, self.mandi.mandi_name_en)

    def __aggregator__(self):
        return "%s" % (self.aggregator.name)

    class Meta:
        unique_together = ("date", "gaddidar", "aggregator", "mandi")


class IncentiveParameter(models.Model):
    notation = models.CharField(max_length=3)
    parameter_name = models.CharField(max_length=25)
    notation_equivalent = models.CharField(max_length=50)

    class Meta:
        unique_together = ("notation", "parameter_name", "notation_equivalent")


class IncentiveModel(models.Model):
    calculation_method = models.TextField()
    description = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.description)


class AggregatorIncentive(LoopModel):
    aggregator = models.ForeignKey(LoopUser)
    start_date = models.DateField(auto_now=False)
    model_type = models.IntegerField(choices=MODEL_TYPES)
    incentive_model = models.ForeignKey(IncentiveModel)

    class Meta:
        unique_together = ("start_date", "aggregator", "model_type", "incentive_model")

    def __unicode__(self):
        return "%s" % (self.aggregator.name)

    def __incentive_model__(self):
        return "%s" % (self.incentive_model.description)


class AggregatorShareOutliers(LoopModel):
    aggregator = models.ForeignKey(LoopUser)
    mandi = ChainedForeignKey(Mandi, chained_field="aggregator", chained_model_field="assigned_mandis")
    date = models.DateField(auto_now=False)
    amount = models.FloatField()
    comment = models.CharField(max_length=200, null=True, blank=True)
    # loop_user = models.ForeignKey(LoopUser,null=True,related_name="loopuser")

    def __mandi__(self):
        return "%s" % (self.mandi.mandi_name)

    def __aggregator__(self):
        return "%s" % (self.aggregator.name)

    class Meta:
        unique_together = ("date", "aggregator", "mandi")


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False, default=datetime.datetime.utcnow)
    user = models.ForeignKey(User, null=True)
    loop_user = models.ForeignKey(LoopUser, null=True)
    village = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)


class AdminLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False, default=datetime.datetime.utcnow)
    user = models.ForeignKey(User, null=True)
    admin_user = models.ForeignKey(AdminUser, null=True)
    district = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)


class HelplineExpert(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email_id = models.CharField(max_length=50)
    expert_status = models.IntegerField(choices=EXPERT_STATUS, default=1)
    state = models.ForeignKey(State, null=True, blank=True)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.phone_number)


class HelplineIncoming(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100)
    from_number = models.CharField(max_length=20, db_index=True)  #User No.
    to_number = models.CharField(max_length=20)  #DG Exotel No.
    incoming_time = models.DateTimeField()
    last_incoming_time = models.DateTimeField()
    resolved_time = models.DateTimeField(null=True, blank=True)
    call_status = models.IntegerField(choices=CALL_STATUS, default=0, db_index=True)
    recording_url = models.CharField(max_length=200, null=True, blank=True)
    resolved_by = models.ForeignKey(HelplineExpert, null=True, blank=True)
    acknowledge_user = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.from_number, self.incoming_time)

    class Meta:
        unique_together = ("call_id", "from_number", "incoming_time")


class HelplineOutgoing(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100)
    incoming_call = models.ForeignKey(HelplineIncoming)
    from_number = models.ForeignKey(HelplineExpert)  #DG Expert No.
    to_number = models.CharField(max_length=20)  #User No.
    outgoing_time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s)" % (self.from_number, self.to_number)

    class Meta:
        unique_together = ("call_id", "incoming_call", "from_number", "outgoing_time")


class HelplineCallLog(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100)
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=20)
    call_type = models.IntegerField(choices=CALL_TYPES)
    start_time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s) (%s)" % (self.from_number, self.to_number, self.call_type)


class HelplineSmsLog(LoopModel):
    id = models.AutoField(primary_key=True)
    sms_id = models.CharField(max_length=100)
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=20)
    sms_body = models.CharField(max_length=2000, null=True, blank=True)
    sent_time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s) (%s)" % (self.from_number, self.to_number, self.sent_time)


class LogDeleted(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False, default=datetime.datetime.now)
    entry_table = models.CharField(max_length=100)
    table_object = models.CharField(max_length=500)


class Broadcast(LoopModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    cluster = models.ManyToManyField(LoopUser)
    audio_url = models.CharField(max_length=130)
    from_number = models.CharField(max_length=20)  #Exotel No.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.start_time)


class BroadcastAudience(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100, blank=True, null=True)
    to_number = models.CharField(max_length=20, db_index=True)  #User No.
    broadcast = models.ForeignKey(Broadcast, blank=True, null=True)
    farmer = models.ForeignKey(Farmer, blank=True, null=True)
    status = models.IntegerField(choices=BROADCAST_STATUS, default=0, db_index=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.to_number, self.broadcast)


class SmsLog(LoopModel):
    id = models.AutoField(primary_key=True)
    sms_body = models.CharField(max_length=1000,null=True,blank=True)
    text_local_id = models.CharField(max_length=20, blank=True, null=True)
    contact_no = models.CharField(max_length=13, blank=True, null=True)
    person_type = models.IntegerField(choices=PERSON_TYPE, default=0)
    status = models.IntegerField(choices=SMS_STATUS, default=0)
    model_ids = models.CharField(default='', max_length=100, null=True, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.contact_no, self.sms_body)
