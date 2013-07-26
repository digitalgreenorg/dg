from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateField("Date Published on")
    source = models.CharField(max_length = 300)
    location = models.CharField(max_length = 200)
    content = models.TextField()
    link = models.URLField(max_length = 1000)
    
    
    def __unicode__(self):
        return '%s' %(self.title)
