import datetime
import urllib2

from django.db import models
from django.db.models.signals import pre_save

from poster.streaminghttp import register_openers
from poster.encode import multipart_encode

from coco.models import CocoUser
from people.models import Person
from dimagi.scripts.create_user import create_dimagi_user

error_list = dict({
                   'SUCCESS'               : 0,
                   'UNIDENTIFIED_FORM'     : -1,
                   'SCREENING_SAVE_ERROR'  : -2,
                   'SCREENING_READ_ERROR'  : -3,
                   'ADOPTION_SAVE_ERROR'   : -4,
                   'ADOPTION_READ_ERROR'   : -5,
                   'PMA_SAVE_ERROR'        : -6,
                   'DEVICE_REPORT'         : -7,
                   'USER_NOT_FOUND'        : -8,
                   'DUPLICATE_SCREENING'   : -9,
                   'DUPLICATE_ADOPTION'    : -10,
                   })

class XMLSubmission(models.Model):
    submission_time = models.DateTimeField(editable=False)
    modification_time = models.DateTimeField(auto_now_add=True)
    xml_data = models.TextField()
    error_code = models.IntegerField(null=True)
    error_message = models.TextField(null=True)
    username = models.CharField(max_length=40, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, default='')
    app_version = models.IntegerField(default='0')

class CommCareProject(models.Model):
    name = models.CharField(max_length=100, unique='True')
    last_updated_time = models.DateTimeField(default=datetime.datetime.utcnow)
    
    def _get_fixture_url(self):
        "Returns the url for the project's fixtures."
        return 'https://www.commcarehq.org/a/%s/fixtures/data-types/' % (self.name)
    fixture_url = property(_get_fixture_url)
    
    def _get_upload_fixture_url(self):
        "Returns the upload url for the project's fixtures."
        return 'https://www.commcarehq.org/a/%s/fixtures/item-lists/upload/' % (self.name)
    upload_fixture_url = property(_get_upload_fixture_url)
    
    def _get_receiver_url(self):
        "Returns the url to upload the project's cases."
        return 'https://www.commcarehq.org/a/%s/receiver' % (self.name)
    receiver_url = property(_get_receiver_url)

    def upload_case_file(self, file):
        register_openers()
        datagen, headers = multipart_encode({"xml_submission_file": open(file, "r")})
        request = urllib2.Request(self.receiver_url , datagen, headers)
        response = urllib2.urlopen(request)
        return response.getcode()
    
    def __unicode__(self):
        return self.name


class CommCareUser(models.Model):
    username = models.CharField(max_length=40)
    guid = models.CharField(max_length=100)
    coco_user = models.ForeignKey(CocoUser)
    project = models.ForeignKey(CommCareProject)

    class Meta:
        unique_together = ("project", "username")

    def __unicode__(self):
        return self.username
pre_save.connect(create_dimagi_user, sender=CommCareUser)

class CommCareCase(models.Model):
    guid = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    person = models.ForeignKey(Person)
    project = models.ForeignKey(CommCareProject)
    user = models.ForeignKey(CommCareUser)
    class Meta:
       unique_together = ("is_open","person","project","user")

