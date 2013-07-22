from django.db import models
from django.contrib.auth.models import User

class FullDownloadStats(models.Model):
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
