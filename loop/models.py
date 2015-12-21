from django.db import models

class Upload(models.Model):
	id = models.AutoField(primary_key=True)
	mediator = models.CharField(max_length=50)
	data = models.CharField(max_length=5000)
	type = models.CharField(max_length=50, null=True, default=None)

	def __unicode__(self):
		return self.mediator

