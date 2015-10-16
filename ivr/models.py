from django.db import models

from geographies.models import District

from dg.base_settings import MEDIA_ROOT

IVR_SERVICE = (
        ('hello', 'hello'),
        ('greeting', 'greeting'),
        ('jharkhand_pilot', 'jharkhand_pilot'),
)

AUDIO_STATUS = (
        ('1', 'Active'),
        ('0', 'InActive'),
)

# Create your models here.
class Call(models.Model):
    exotel_call_id = models.CharField(max_length=100)
    attributes = models.TextField(max_length=5000)
    state = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
        
    def attempt(self, call_dict):
        # call data to be initialized when a call is attmepted
        # self.duration = call_dict['Duration']
        # self.to = call_dict['To']
        # self.from = call_dict['From']
        # self.attributes = props
            #date_updated = models.DateTimeField()
            #startTime
            #endTime
        return None
    
    def end(self, response):
        # arguments are a dictionary of relevant data
        # this function adds the information and saves it in the db
        # http://support.exotel.in/support/solutions/articles/48278-outbound-call-to-connect-a-customer-to-an-app
        self.attributes = response
        self.save()
        return None

class Audio(models.Model):
    audio_file = models.FileField(upload_to=MEDIA_ROOT+'ivrs/')
    title = models.CharField(max_length=100)
    meta = models.TextField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    audio_status = models.CharField(max_length=20, choices=AUDIO_STATUS)

class Broadcast(models.Model):
    service = models.CharField(max_length=20, choices=IVR_SERVICE)
    audio_file = models.ForeignKey(Audio)
    district = models.ManyToManyField(District)
    schedule_call = models.DateTimeField()    
