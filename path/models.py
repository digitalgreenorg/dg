from django.db import models
from dashboard.models import Person
from dashboard.fields import *
# Create your models here.
MIN_ONLINE = 10000000000000
class PathLog(models.Model):
    id = BigAutoField(primary_key = True)
    person_offline_id = models.BigIntegerField()
    person_online_id = models.BigIntegerField()
    read = models.BooleanField(default=False)
