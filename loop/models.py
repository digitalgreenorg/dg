import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from loop_data_log import save_log, delete_log

RoleChoice = ((1, "Admin"), (2, "Aggregator"), (3, "Testing"))
ModelChoice = ((1, "Direct Sell"),  (2, "Aggregate"))
DISCOUNT_CRITERIA = ((0, "Volume"), (1, "Amount"))


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

    def __unicode__(self):
        return self.state_name

    class Meta:
        unique_together = ("state_name",)


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
    role = models.IntegerField(choices=RoleChoice)
    assigned_villages = models.ManyToManyField(
        Village, related_name="assigned_villages", through='LoopUserAssignedVillage', blank=True)
    assigned_mandis = models.ManyToManyField(
        Mandi, related_name="assigned_mandis", through='LoopUserAssignedMandi', blank=True)
    mode = models.IntegerField(choices=ModelChoice, default=1)
    phone_number = models.CharField(
        max_length=14, null=False, blank=False, default="0")
    village = models.ForeignKey(Village, default=None, null=True)
    name_en = models.CharField(max_length=100, null=True)
    preferred_language = models.ForeignKey(Language, null=True)
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def get_villages(self):
        return self.assigned_villages.all()

    def get_mandis(self):
        return self.assigned_mandis.all()


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
    commission = models.FloatField(default=1.0)
    mandi = models.ForeignKey(Mandi)
    is_visible = models.BooleanField(default=True)
    gaddidar_name_en = models.CharField(max_length=100, null=True)
    discount_criteria = models.IntegerField(choices=DISCOUNT_CRITERIA, default=0)

    def __unicode__(self):
        return self.gaddidar_name

    class Meta:
        unique_together = ("gaddidar_phone", "gaddidar_name")

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
        unique_together = ("phone", "name")

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
    crop = models.ForeignKey(Crop)
    crop_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.crop_name
    def __crop__(self):
        return "%s" % (self.crop.crop_name)

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


class TransportationVehicle(LoopModel):
    id = models.AutoField(primary_key=True)
    transporter = models.ForeignKey(Transporter)
    vehicle = models.ForeignKey(Vehicle)
    vehicle_number = models.CharField(max_length=20)
    is_visible = models.BooleanField(default=True)

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
    comment = models.CharField(max_length=200, null=True, blank=True)
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
    gaddidar = models.ForeignKey(Gaddidar)
    start_date = models.DateField(auto_now=False)
    discount_percent = models.FloatField(validators=[MinValueValidator(0.0),
                                                     MaxValueValidator(1.0)], default=0.0)
    def __unicode__(self):
        return "%s (%s)" % (
            self.gaddidar.gaddidar_name, self.mandi.mandi_name)

    class Meta:
        unique_together = ("start_date", "gaddidar", "mandi")

class GaddidarShareOutliers(LoopModel):
    mandi = models.ForeignKey(Mandi)
    gaddidar = models.ForeignKey(Gaddidar)
    aggregator = models.ForeignKey(LoopUser)
    date = models.DateField(auto_now=False)
    amount = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (
            self.gaddidar.gaddidar_name, self.mandi.mandi_name)

    def __aggregator__(self):
        return "%s" % (LoopUser.objects.get(user=self.user_created).name)

    class Meta:
        unique_together = ("date", "gaddidar", "aggregator", "mandi")

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
