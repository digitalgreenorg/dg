from django.contrib.auth.models import User

from django.db import models
from geographies.models import State, District
from videos.models import Language
from people.models import Animator
from programs.models import Partner

# Create your models here.

class TrainingUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="training_user")
    states = models.ManyToManyField(State)

    def __unicode__(self):
    	return self.user.username

    def get_states(self):
    	return self.states.all()

class Trainer(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	language = models.ForeignKey(Language, null=True, blank=True)

	def __unicode__(self):
		return self.name

class Assessment(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Question(models.Model):
	id = models.AutoField(primary_key=True)
	assessment = models.ForeignKey(Assessment, null=True, blank=True)
	language = models.ForeignKey(Language, null=True, blank=True)
	section = models.IntegerField()
	serial = models.IntegerField()
	text = models.CharField(max_length = 100)

	def __unicode__(self):
		return self.text

class Training(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
	place = models.CharField(max_length=200)
	assessment = models.ForeignKey(Assessment, null=True, blank=True)
	trainer = models.ManyToManyField(Trainer, blank=True)
	language = models.ForeignKey(Language, null=True, blank=True)
	participants = models.ManyToManyField(Animator)
	district = models.ForeignKey(District, null=True, blank=True)
	trainingType = models.BooleanField(default=True)
	partner = models.ForeignKey(Partner, null=True, blank=True)

	# class Meta:
 #    	unique_together=("date","trainer")

class Score(models.Model):
	id = models.AutoField(primary_key=True)
	training = models.ForeignKey(Training)
	participant = models.ForeignKey(Animator)
	question = models.ForeignKey(Question)
	score = models.IntegerField()

	class Meta:
		unique_together=("training", "participant", "question")
