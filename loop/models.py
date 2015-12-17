from django.db import models

class Upload(models.Model):
	id = models.AutoField(primary_key=True)
	data = models.CharField(max_length=5000)
	mediator = models.CharField(max_length=50)

