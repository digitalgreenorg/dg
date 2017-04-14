from django.contrib.auth.models import User

from django.db import models
from geographies.models import State, District
from videos.models import Language
from people.models import Animator
from programs.models import Partner
from datetime import datetime
from django.db.models.signals import pre_delete, post_save
from training.log.training_log import enter_to_log
# Create your models here.

class TrainingUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, related_name="training_user")
    states = models.ManyToManyField(State)

    def __unicode__(self):
    	return self.user.username

    def get_states(self):
    	return self.states.all()

class BaseModel(models.Model):
	user_created = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created", editable=False, null=True, blank=True)
	time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	user_modified = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related_modified", editable=False, null=True, blank=True)
	time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		abstract = True

class Trainer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    language = models.ForeignKey(Language, null=True, blank=True)
    training_user = models.ForeignKey(TrainingUser, null=True, blank=True)

    def __training_user__(self):
        return "%s" % (self.training_user.id)

    def __unicode__(self):
        return self.name

post_save.connect(enter_to_log, sender=Trainer)
pre_delete.connect(enter_to_log, sender=Trainer)

class Assessment(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

post_save.connect(enter_to_log, sender=Assessment)
pre_delete.connect(enter_to_log,sender=Assessment)

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    assessment = models.ForeignKey(Assessment, null=True, blank=True)
    language = models.ForeignKey(Language, null=True, blank=True)
    section = models.IntegerField()
    serial = models.IntegerField()
    text = models.CharField(max_length = 100)
    tag = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return self.text

    def __assessment__(self):
        return "%s"% (self.assessment.name)

post_save.connect(enter_to_log, sender=Question)
pre_delete.connect(enter_to_log,sender=Question)

class Training(BaseModel):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    place = models.CharField(max_length=200)
    assessment = models.ForeignKey(Assessment, null=True, blank=True)
    trainer = models.ManyToManyField(Trainer, blank=True)
    facilitator = models.ForeignKey(Trainer, blank=True, null=True, related_name="facilitator")
    language = models.ForeignKey(Language, null=True, blank=True)
    participants = models.ManyToManyField(Animator)
    district = models.ForeignKey(District, null=True, blank=True)
    trainingType = models.BooleanField(default=True,verbose_name="Without Video") # with / without video
    kind_of_training = models.BooleanField(default=True, verbose_name="New Training") # new / refresher training
    participants_count = models.IntegerField(default=0)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    def trainers(self):
        return " , ".join([t.name for t in self.trainer.all()])

post_save.connect(enter_to_log, sender=Training)
pre_delete.connect(enter_to_log,sender=Training)

class Score(models.Model):
	id = models.AutoField(primary_key=True)
	training = models.ForeignKey(Training)
	participant = models.ForeignKey(Animator)
	question = models.ForeignKey(Question)
	score = models.IntegerField()

	class Meta:
		unique_together=("training", "participant", "question")

post_save.connect(enter_to_log, sender=Score)
pre_delete.connect(enter_to_log,sender=Score)

class LogData(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False, default=datetime.now)
    user = models.ForeignKey(User, null=True)
    action = models.IntegerField()
    entry_table = models.CharField(max_length=100)
    model_id = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Logs"

class DeleteLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=False, default=datetime.now)
    entry_table = models.CharField(max_length=100)
    table_object = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = "Deleted Logs"
