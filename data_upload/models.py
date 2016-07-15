from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Document(models.Model):
    docfile = models.FileField(upload_to='documents')
    upload_DateTime = models.DateTimeField(default=datetime.datetime.utcnow)
    user_id = models.ForeignKey(User)
    

