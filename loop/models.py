# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from loop_data_log import save_log, delete_log
from smart_selects.db_fields import ChainedForeignKey
from constants.constants import *

ROLE_CHOICE = ((ROLE_CHOICE_ADMIN, "Admin"), (ROLE_CHOICE_AGGREGATOR, "Aggregator"), (ROLE_CHOICE_TESTING, "Testing"))
MODEL_CHOICE = ((1, "Direct Sell"),  (2, "Aggregate"))
DISCOUNT_CRITERIA = ((DISCOUNT_CRITERIA_VOLUME, "Volume"), (DISCOUNT_CRITERIA_AMOUNT, "Amount"))
MODEL_TYPES = ((MODEL_TYPES_DIRECT, "Direct"), (MODEL_TYPES_TAX_BASED, "Tax Based"), (MODEL_TYPES_SLAB_BASED, "Slab Based"), (MODEL_TYPES_DAILY_PAY, "Daily Pay"))
CALL_TYPES = ((0, "Incoming"), (1, "Outgoing"))
CALL_STATUS = ((0, "Pending"),  (1, "Resolved"), (2, "Declined"))
EXPERT_STATUS = ((0, "Inactive"), (1, "Active"))
BROADCAST_STATUS = ((0, "Pending"), (1, "Done"), (2, "DND-Failed"), (3, "Declined"))

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
    state_name_en = models.CharField(max_length=100, null=True)
    helpline_number = models.CharField(max_length=14, null=False, blank=False, default="0")
    crop_add = models.BooleanField(default=False)
    phone_digit = models.CharField(default=10, max_length=2, blank=True, null=True)
    phone_start = models.CharField(default=789, max_length=15, blank=True, null=True)
    def __unicode__(self):
        return self.state_name

    class Meta:
        unique_together = ("state_name",)

post_save.connect(save_log,sender=State)
pre_delete.connect(delete_log,sender=State)

class District(LoopModel):
    id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=50)
    state = models.ForeignKey(State)
    is_visible = models.BooleanField(default=True)
    district_name_en = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.district_name, self.state.state_name)

    class Meta:
        unique_together = ("district_name", "state")


class Block(LoopModel):
    id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=50)
    district = models.ForeignKey(District)
    is_visible = models.BooleanField(default=True)
    block_name_en = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.block_name, self.district.district_name)

    class Meta:
        unique_together = ("block_name", "district")


class Village(LoopModel):
    id = models.AutoField(primary_key=True)
    village_name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    block = models.ForeignKey(Block)
    is_visible = models.BooleanField(default=True)
    village_name_en = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.village_name, self.block.block_name)

    class Meta:
        unique_together = ("village_name", "block")


post_save.connect(save_log, sender=Village)
pre_delete.connect(delete_log, sender=Village)


class Mandi(LoopModel):
    id = models.AutoField(primary_key=True)
    mandi_name = models.CharField(max_length=90)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    district = models.ForeignKey(District)
    is_visible = models.BooleanField(default=True)
    mandi_name_en = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.mandi_name, self.district.district_name)

    class Meta:
        unique_together = ("mandi_name", "district",)

post_save.connect(save_log, sender=Mandi)
pre_delete.connect(delete_log, sender=Mandi)


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
    name_en = models.CharField(max_length=100, null=True)
    preferred_language = models.ForeignKey(Language, null=True)
    days_count = models.IntegerField(default=3)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_villages(self):
        return self.assigned_villages.all()

    def get_mandis(self):
        return self.assigned_mandis.all()

    def __user__(self):
        return "%s" % self.user.id

post_save.connect(save_log,sender=LoopUser)
pre_delete.connect(delete_log,sender=LoopUser)

class LoopUserAssignedMandi(LoopModel):
    id = models.AutoField(primary_key=True)
    loop_user = models.ForeignKey(LoopUser)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)

post_save.connect(save_log, sender=LoopUserAssignedMandi)
pre_delete.connect(delete_log, sender=LoopUserAssignedMandi)


class LoopUserAssignedVillage(LoopModel):
    id = models.AutoField(primary_key=True)
    loop_user = models.ForeignKey(LoopUser)
    village = models.ForeignKey(Village)
    is_visible = models.BooleanField(default=True)

post_save.connect(save_log, sender=LoopUserAssignedVillage)
pre_delete.connect(delete_log, sender=LoopUserAssignedVillage)


class Gaddidar(LoopModel):
    id = models.AutoField(primary_key=True)
    gaddidar_name = models.CharField(max_length=100)
    gaddidar_phone = models.CharField(max_length=13)
    commission = models.FloatField("Discount",default=1.0)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)
    gaddidar_name_en = models.CharField(max_length=100, null=True)
    discount_criteria = models.IntegerField(choices=DISCOUNT_CRITERIA, default=0)

    def __unicode__(self):
        return self.gaddidar_name

    class Meta:
        unique_together = ("gaddidar_phone", "gaddidar_name","mandi")

post_save.connect(save_log, sender=Gaddidar)
pre_delete.connect(delete_log, sender=Gaddidar)


class Farmer(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)  # M/F
    phone = models.CharField(max_length=13)
    image_path = models.CharField(
        max_length=500, default=None, null=True, blank=True)
    village = models.ForeignKey(Village)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.village.village_name)

    def __village__(self):
        return "%s" % (self.village.village_name)

    class Meta:
        unique_together = ("phone", "name", "village")

post_save.connect(save_log, sender=Farmer)
pre_delete.connect(delete_log, sender=Farmer)


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
pre_delete.connect(delete_log, sender=Crop)

#############Crop name in multiple languages###############

class CropLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,null=True)
    crop = models.ForeignKey(Crop, related_name="crops")
    crop_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.crop_name
    def __crop__(self):
        return "%s" % (self.crop.crop_name)

post_save.connect(save_log,sender=CropLanguage)
pre_delete.connect(delete_log,sender=CropLanguage)

class Transporter(LoopModel):
    id = models.AutoField(primary_key=True)
    transporter_name = models.CharField(max_length=90)
    transporter_phone = models.CharField(max_length=13)
    block = models.ForeignKey(Block)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.transporter_name)

    def __block__(self):
        return "%s" % (self.block.block_name)

    class Meta:
        unique_together = ("transporter_name", "transporter_phone",)

post_save.connect(save_log, sender=Transporter)
pre_delete.connect(delete_log, sender=Transporter)


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
pre_delete.connect(delete_log, sender=Vehicle)

class VehicleLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language,null=True)
    vehicle = models.ForeignKey(Vehicle, related_name="vehicles")
    vehicle_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.vehicle_name
    def __crop__(self):
        return "%s" % (self.vehicle.vehicle_name)

post_save.connect(save_log,sender=VehicleLanguage)
pre_delete.connect(delete_log,sender=VehicleLanguage)


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
pre_delete.connect(delete_log, sender=TransportationVehicle)


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

    def __unicode__(self):
        return "%s - %s (%s)" % (LoopUser.objects.get(user=self.user_created).name, self.transportation_vehicle.transporter.transporter_name, self.transportation_vehicle.vehicle.vehicle_name)

    def __aggregator__(self):
        return "%s" % (LoopUser.objects.get(user=self.user_created).name)

    def __transporter__(self):
        return "%s" % (self.transportation_vehicle.transporter.transporter_name)

    def __vehicle__(self):
        return "%s (%s)" % (self.transportation_vehicle.vehicle.vehicle_name, self.transportation_vehicle.vehicle_number)

    def __mandi__(self):
        return "%s" % (self.mandi.mandi_name)

    class Meta:
        unique_together = ("date", "user_created", "timestamp")

post_save.connect(save_log, sender=DayTransportation)
pre_delete.connect(delete_log, sender=DayTransportation)


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

    def __unicode__(self):
        return "%s (%s) (%s) (%s)" % (
            self.farmer.name, self.crop.crop_name, self.mandi.mandi_name,
            LoopUser.objects.get(user=self.user_created).name)

    def __aggregator__(self):
        return "%s" % (LoopUser.objects.get(user=self.user_created).name)

    def __farmer__(self):
        return "%s" % (self.farmer.name)

    def __crop__(self):
        return "%s" % (self.crop.crop_name)

    def __mandi__(self):
        return "%s" % (self.mandi.mandi_name)

    def __gaddidar__(self):
        return "%s" % (self.gaddidar.gaddidar_name)

    class Meta:
        unique_together = ("date", "user_created", "timestamp")


post_save.connect(save_log, sender=CombinedTransaction)
pre_delete.connect(delete_log, sender=CombinedTransaction)

class GaddidarCommission(LoopModel):
    mandi = models.ForeignKey(Mandi)
    gaddidar = ChainedForeignKey(Gaddidar, chained_field="mandi", chained_model_field="mandi")
    start_date = models.DateField(auto_now=False)
    discount_percent = models.FloatField(verbose_name="Discount",validators=[MinValueValidator(0.0),
                                                     MaxValueValidator(1.0)], default=0.0)
    def __unicode__(self):
        return "%s (%s)" % (
            self.gaddidar.gaddidar_name, self.mandi.mandi_name)

    class Meta:
        unique_together = ("start_date", "gaddidar", "mandi")
post_save.connect(save_log, sender=GaddidarCommission)
pre_delete.connect(delete_log, sender=GaddidarCommission)

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
            self.gaddidar.gaddidar_name, self.mandi.mandi_name)

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
    calculation_method = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.calculation_method)

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
        return "%s" % (self.incentive_model.calculation_method)

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
        unique_together = ("date","aggregator","mandi")

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(
        auto_now_add=False, default=datetime.datetime.utcnow)
    user = models.ForeignKey(User, null=True)
    loop_user = models.ForeignKey(LoopUser, null=True)
    village = models.IntegerField(null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)


class HelplineExpert(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email_id = models.CharField(max_length=50)
    expert_status = models.IntegerField(choices=EXPERT_STATUS, default=1)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.phone_number)


class HelplineIncoming(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100)
    from_number = models.CharField(max_length=20, db_index=True) #User No.
    to_number = models.CharField(max_length=20)                  #DG Exotel No.
    incoming_time = models.DateTimeField()
    last_incoming_time = models.DateTimeField()
    resolved_time = models.DateTimeField(null=True, blank=True)
    call_status = models.IntegerField(choices=CALL_STATUS, default=0, db_index=True)
    recording_url = models.CharField(max_length=200, null=True , blank=True)
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
    from_number = models.ForeignKey(HelplineExpert) #DG Expert No.
    to_number = models.CharField(max_length=20)     #User No.
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
    sms_body = models.CharField(max_length=2000,null=True,blank=True)
    sent_time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s) (%s)" % (self.from_number, self.to_number, self.sent_time)


class Broadcast(LoopModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    cluster = models.ManyToManyField(LoopUser)
    audio_url = models.CharField(max_length=130)
    from_number = models.CharField(max_length=20)     #Exotel No.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.start_time)


class BroadcastAudience(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100, blank=True, null=True)
    to_number = models.CharField(max_length=20, db_index=True)       #User No.
    broadcast = models.ForeignKey(Broadcast, blank=True, null=True)
    farmer = models.ForeignKey(Farmer, blank=True, null=True)
    status = models.IntegerField(choices=BROADCAST_STATUS, default=0, db_index=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.to_number, self.broadcast)
