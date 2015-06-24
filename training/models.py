from django.db import models
from geographies.models import State
from videos.models import Language
from people.models import Animator

# Create your models here.
class Trainer(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	state = models.ForeignKey(State, null=True, blank=True)

class Module(models.Model):
	id = models.AutoField(primary_key=True)
	module_name = models.CharField(max_length=50)

class Question(models.Model):
	id = models.AutoField(primary_key=True)
	module = models.ForeignKey(Module, null=False, blank=False)
	language = models.ForeignKey(Language, null=False, blank=False)
	question_number = models.IntegerField()
	question_text = models.CharField(max_length=200)


class Training(models.Model):
	id = models.AutoField(primary_key=True)
	taining_date = models.DateField()
	place = models.CharField(max_length=200)
	trainer = models.ManyToManyField(Trainer, null=False, blank=False)
	language = models.ForeignKey(Language, null=False, blank=False)

class MediatorScore(models.Model):
	id = models.AutoField(primary_key=True)
	training = models.ForeignKey(Training, null=False, blank=False)
	animator = models.ForeignKey(Animator, null=False, blank=False)
	question = models.ForeignKey(Question, null=False, blank=False)
	score = models.IntegerField()









