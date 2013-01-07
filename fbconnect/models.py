from django.db import models
from dashboard.models import Person
from dashboard.fields import BigAutoField, BigForeignKey, PositiveBigIntegerField
# Create your models here.

class FBUser(models.Model):
    fuid = models.CharField(max_length=64)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'fb_user'

class FBFollowers(models.Model):
    fbuser = models.CharField(max_length=64, null=True)
    person = PositiveBigIntegerField(null=True)
    
    class Meta:
        db_table = 'fb_followers'