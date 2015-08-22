from django.db import models

# Create your models here.
class Call(models.Model):
    exotel_call_id = models.CharField(max_length=100)
    attributes = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
