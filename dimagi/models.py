from django.db import models

class XMLSubmission(models.Model):
    submission_time = models.DateTimeField(auto_now=True)
    modification_time = models.DateTimeField(auto_now_add=True)
    xml_data = models.TextField()
