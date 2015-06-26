from django.db import models
from geographies.models import State
from videos.models import Language
from people.models import Animator

# Create your models here.
class Trainer(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()

class Question(models.Model):
	id = models.AutoField(primary_key=True)
	assessment = models.ForeignKey(Assessment, null=False, blank=False)
	section = models.IntegerField()
	serial = models.IntegerField()
	text = models.CharField()

class Translation(models.Model):
	question = models.ForeignKey(Question, null=False, blank=False)
	text = models.CharField()
	language = models.ForeignKey(Language, null=False, blank=False)

class Assessment(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

class Training(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
	place = models.CharField(max_length=200)
	state = models.ForeignKey(State, null=True, blank=True)
	trainer = models.ManyToManyField(Trainer, null=False, blank=False)
	language = models.ForeignKey(Language, null=False, blank=False)
	participants = ManyToManyField(Animator)

class Score(models.Model):
	id = models.AutoField(primary_key=True)
	training = models.ForeignKey(Training, null=False, blank=False)
	participant = models.ForeignKey(Animator, null=False, blank=False)
	question = models.ForeignKey(Question, null=False, blank=False)
	score = models.IntegerField()






