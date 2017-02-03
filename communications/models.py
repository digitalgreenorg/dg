from django.db import models
from django.utils import timezone
import datetime


class Article(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField("Date Published on")
    source = models.CharField(max_length = 300)
    location = models.CharField(max_length = 200)
    content = models.TextField()
    link = models.URLField(max_length = 1000)

    def __unicode__(self):
        return '%s' %(self.title)

class Feedback(models.Model):
    rating = models.IntegerField(default=5)
    comments = models.CharField(max_length=1000)
    email = models.EmailField(max_length=254)
    date = models.DateField(default=timezone.now)
    time = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        verbose_name_plural = "Feedback"
