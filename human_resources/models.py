from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

team_choices = [('Executive Leadership Team', 'Executive Leadership Team'),
                ('Technology Team', 'Technology Team'),
                ('Program Team', 'Program Team'),
                ('Support Team', 'Support Team')]

location_choices = [('Headquarters-Delhi', 'Headquarters-Delhi'),
                    ('Bangalore', 'Bangalore'),
                    ('Bhopal', 'Bhopal'),
                    ('Bhubaneswar', 'Bhubaneswar'),
                    ('Hyderabad', 'Hyderabad'),
                    ('Patna', 'Patna')]

# Models for Team page
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)  # all possible valid e-mails
    designation = models.CharField(max_length=100)  # Designation
    personal_intro = models.TextField(help_text="""Minimum Length Should be 250
                                                 and Maximum 1350""",
                                      validators=[MaxLengthValidator(1350),
                                                  MinLengthValidator(250)])
    team = models.CharField(max_length=100, choices=team_choices)
    location = models.CharField(max_length=100, choices=location_choices)
    image = models.ImageField(help_text="""Minimum Width Should be 100
                                         and Minimum Height should be 100""",
                              upload_to='team/')
    hierarchy_num = models.FloatField()
    def __unicode__(self):
        return self.name

# Models for Careers page

class Job(models.Model):
    title = models.CharField(max_length = 300)
    description = models.TextField()
    conclusion = models.TextField()
    hierarchy_num = models.FloatField(default=0)
    
    def __unicode__(self):
        return '%s' %(self.title)

class KeyResponsibility(models.Model):
    job = models.ForeignKey(Job)
    point = models.CharField(max_length = 500)
    
    def __unicode__(self):
        return '%s' %(self.point)

class ExperienceQualification(models.Model):
    job = models.ForeignKey(Job)
    point = models.CharField(max_length = 500)
    
    def __unicode__(self):
        return '%s' %(self.point)
