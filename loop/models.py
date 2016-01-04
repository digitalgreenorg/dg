
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

RoleChoice = ((1, "Admin"), (2, "Aggregator"))

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

class State(LoopModel):
	id = models.AutoField(primary_key=True)
	state_name = models.CharField(max_length=50)
	country = models.ForeignKey(Country)

	def __unicode__(self):
		return self.state_name

class District(LoopModel):
	id = models.AutoField(primary_key=True)
	district_name = models.CharField(max_length=50)
	state = models.ForeignKey(State)
		
	def __unicode__(self):
		return self.district_name

class Block(LoopModel):
	id = models.AutoField(primary_key=True)
	block_name = models.CharField(max_length=50)
	district = models.ForeignKey(District)

	def __unicode__(self):
		return self.block_name

class Village(LoopModel):
	id = models.AutoField(primary_key=True)
	village_name = models.CharField(max_length=50)
	latitude = models.FloatField(null=True)
	longitude = models.FloatField(null=True)
	block = models.ForeignKey(Block)
	
	def __unicode__(self):
		return self.village_name

class LoopUser(LoopModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="loop_user")
    role = models.IntegerField(choices = RoleChoice)
    assigned_villages = models.ManyToManyField(Village, related_name="assigned_villages")

    def __unicode__(self):
    	return self.user.username

class Farmer(LoopModel):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
#	gender = models.CharField(max_length=1)		# M/F
	phone = models.CharField(max_length=13)
	image_path = models.CharField(max_length=100)
	village = models.ForeignKey(Village)

	def __unicode__(self):
		return self.name;

class Crop(LoopModel):
	id = models.AutoField(primary_key=True)
	crop_name = models.CharField(max_length=30)
	measuring_unit = models.CharField(max_length=20)
	image_path = models.CharField(max_length=100)
		
	def __unicode__(self):
		return self.crop_name

class Mandi(LoopModel):
	id = models.AutoField(primary_key=True)
	mandi_name = models.CharField(max_length=90)
	latitude = models.FloatField(null=True)
	longitude =  models.FloatField(null=True)
	district = models.ForeignKey(District)
		
	def __unicode__(self):
		return self.mandi_name

class CombinedTransaction(LoopModel):
 	id = models.AutoField(primary_key=True)
 	date = models.DateField(auto_now=False)
	aggregator = models.ForeignKey(LoopUser)
	farmer = models.ForeignKey(Farmer)
	crop = models.ForeignKey(Crop)
	mandi = models.ForeignKey(Mandi)
	crop_amount = models.FloatField()
	crop_price = models.FloatField()
	pay_status = models.CharField(max_length=1)
	pay_amount = models.FloatField()

	class Meta:
		db_table = 'combined_transaction'

class log(LoopModel):
	id = models.AutoField(primary_key=True)
	user = models.CharField(max_length=50)
	data = models.CharField(max_length=5000)
	timestamp = models.DateTimeField(auto_now=False)
	type = models.CharField(max_length=50, null=True, default=None)

	def __unicode__(self):
		return self.mediator

