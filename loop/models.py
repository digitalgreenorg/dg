import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from loop_data_log import save_log, delete_log

RoleChoice = ((1, "Admin"), (2, "Aggregator"))
ModelChoice = ((1, "Direct Sell"), (2, "Aggregate"))

class LoopModel(models.Model):
    user_created = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_created", editable = False, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(User, related_name ="%(app_label)s_%(class)s_related_modified",editable = False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class Country(LoopModel):
	id = models.AutoField(primary_key=True)
	country_name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.country_name
	class Meta:
		unique_together = ("country_name",)

class State(LoopModel):
	id = models.AutoField(primary_key=True)
	state_name = models.CharField(max_length=50)
	country = models.ForeignKey(Country)

	def __unicode__(self):
		return self.state_name
	class Meta:
		unique_together = ("state_name",)

class District(LoopModel):
    id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=50)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.district_name
    class Meta:
        unique_together = ("district_name","state")

class Block(LoopModel):
	id = models.AutoField(primary_key=True)
	block_name = models.CharField(max_length=50)
	district = models.ForeignKey(District)

	def __unicode__(self):
		return self.block_name
	class Meta:
		unique_together = ("block_name","district")

class Village(LoopModel):
	id = models.AutoField(primary_key=True)
	village_name = models.CharField(max_length=50)
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	block = models.ForeignKey(Block)

	def __unicode__(self):
		return self.village_name
	class Meta:
		unique_together = ("village_name","block")
post_save.connect(save_log, sender=Village)
pre_delete.connect(delete_log, sender=Village)

class LoopUser(LoopModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="loop_user")
    name = models.CharField(max_length=100, default="default");
    role = models.IntegerField(choices = RoleChoice)
    assigned_villages = models.ManyToManyField(Village, related_name="assigned_villages")
    mode = models.IntegerField(choices = ModelChoice, default = 1)
    phone_number = models.CharField(max_length = 14, null = False, blank = False, default = "0")
    village = models.ForeignKey(Village, default=None, null=True)

    def __unicode__(self):
        return self.user.username
    def get_villages(self):
        return self.assigned_villages.all()

class Farmer(LoopModel):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	gender = models.CharField(max_length=1)		# M/F
	phone = models.CharField(max_length=13)
	image_path = models.CharField(max_length = 500 , default = None, null = True, blank=True)
	village = models.ForeignKey(Village)

	def __unicode__(self):
		return self.name;
	class Meta:
		unique_together = ("phone","name")
post_save.connect(save_log, sender=Farmer)
pre_delete.connect(delete_log, sender=Farmer)

class Crop(LoopModel):
	id = models.AutoField(primary_key=True)
	image_path = models.CharField(max_length = 500 , default = None, null = True, blank=True)
	crop_name = models.CharField(max_length=30, null = False, blank = False)
	measuring_unit = models.CharField(max_length=20, default = "kg")

	def __unicode__(self):
		return self.crop_name
	class Meta:
		unique_together = ("crop_name",)
post_save.connect(save_log, sender=Crop)
pre_delete.connect(delete_log, sender=Crop)

class Mandi(LoopModel):
	id = models.AutoField(primary_key=True)
	mandi_name = models.CharField(max_length=90)
	latitude = models.FloatField(null=True)
	longitude =  models.FloatField(null=True)
	district = models.ForeignKey(District)

	def __unicode__(self):
		return self.mandi_name
	class Meta:
		unique_together = ("mandi_name","district",)

class Transporter(LoopModel):
	id = models.AutoField(primary_key=True)
	transporter_name = models.CharField(max_length=90)
	transporter_phone = models.CharField(max_length=13)
	district = models.ForeignKey(District)

	def __unicode__(self):
		return self.transporter_name
	class Meta:
		unique_together = ("transporter_name","transporter_phone",)
post_save.connect(save_log, sender=Transporter)
pre_delete.connect(delete_log, sender=Transporter)

class Vehicle(LoopModel):
	id = models.AutoField(primary_key=True)
	vehicle_name = models.CharField(max_length=30, blank=False, null=False)

	def __unicode__(self):
		return self.vehicle_name
	class Meta:
		unique_together = ("vehicle_name",)

class TransportationVehicle(LoopModel):
	id = models.AutoField(primary_key=True)
	transporter = models.ForeignKey(Transporter)
	vehicle = models.ForeignKey(Vehicle)
	vehicle_number = models.CharField(max_length=11)

	class Meta:
		unique_together = ("transporter", "vehicle", "vehicle_number",)
post_save.connect(save_log, sender=TransportationVehicle)
pre_delete.connect(delete_log, sender=TransportationVehicle)

class DayTransportation(LoopModel):
	id = models.AutoField(primary_key=True)
	date = models.DateField(auto_now=False)
	transportation_vehicle = models.ForeignKey(TransportationVehicle)
	transportation_cost = models.FloatField()
	other_cost = models.FloatField()
	vrp_fees = models.FloatField()
	comment = models.CharField(max_length = 200)
	mandi_list = models.CharField(max_length=20)
post_save.connect(save_log, sender=DayTransportation)
pre_delete.connect(delete_log, sender=DayTransportation)

class CombinedTransaction(LoopModel):
	id = models.AutoField(primary_key=True)
	date = models.DateField(auto_now=False)
	farmer = models.ForeignKey(Farmer)
	crop = models.ForeignKey(Crop)
	mandi = models.ForeignKey(Mandi)
	quantity = models.FloatField()
	price = models.FloatField()
	status = models.IntegerField()
	amount = models.FloatField()
	day_transportation = models.ForeignKey(DayTransportation, default=None, null=True)
	def __unicode__(self):
		return "%s (%s) (%s) (%s)" % (self.farmer.name, self.crop.crop_name, self.mandi.mandi_name, LoopUser.objects.get(user= self.user_created).name)

	class Meta:
		unique_together = ("date","farmer","crop","mandi","price",)
post_save.connect(save_log, sender=CombinedTransaction)
pre_delete.connect(delete_log, sender=CombinedTransaction)

class Log(models.Model):
	id = models.AutoField(primary_key=True)
	timestamp = models.DateTimeField(auto_now_add = False, default=datetime.datetime.utcnow)
	user = models.ForeignKey(User, null=True)
	village = models.IntegerField(null=True)
	action = models.IntegerField()
	entry_table = models.CharField(max_length=100)
	model_id = models.IntegerField(null=True)
