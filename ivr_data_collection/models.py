from django.db import models

# Create your models here.
class CustomFieldTest(models.Model):
	id = models.AutoField(primary_key=True)
	call_sid = models.CharField(max_length=50,null=True)
	mobile_number = models.CharField(max_length=10, null=True)
	CustomField = models.CharField(max_length=20, null=True, default="abc")