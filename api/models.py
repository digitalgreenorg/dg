from django.db import models
from django.contrib.auth.models import Group


class View(models.Model):
    '''
    This is model for View present in the views.py. Groups represent the permitted groups allowed to access it.
    '''
    id = models.AutoField(primary_key=True)
    view_name = models.CharField(max_length=200) 
    permission_groups = models.ManyToManyField(Group)

    def __str__(self):
        "Returns the view name and groups names mapped together"
        return '%s, %s'%(self.view_name, self.permission_groups)
