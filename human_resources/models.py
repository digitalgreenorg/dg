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
    image = models.ImageField(help_text="""Maximum Width Should be 118
                                         and Maximum Height should be 124""",
                              upload_to='team/')

    def __unicode__(self):
        return self.name