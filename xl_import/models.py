from django.db import models
#from django.contrib.auth.models import User

class Document(models.Model):
    docfile = models.FileField(upload_to='documents')
    #upload_date = models.DateTimeField('uploaded date')
    #user_id = models.ForeignKey(User)
    

