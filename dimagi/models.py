from django.db import models
from poster.streaminghttp import register_openers

from dashboard.fields import BigForeignKey
from dashboard.models import Person, Village

error_list = dict({'UNIDENTIFIED_FORM'     : -1,
                   'SCREENING_SAVE_ERROR'  : -2,
                   'SCREENING_READ_ERROR'  : -3,
                   'ADOPTION_SAVE_ERROR'   : -4,
                   'ADOPTION_READ_ERROR'   : -5,
                   'PMA_SAVE_ERROR'        : -6,
                   })

class XMLSubmission(models.Model):
    submission_time = models.DateTimeField(auto_now=True)
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
    
    def _get_fixture_url(self):
        "Returns the url for the project's fixtures."
        return 'https://www.commcarehq.org/a/%s/fixtures/data-types/' % (self.name)
    fixture_url = property(_get_fixture_url)
    
    def _get_receiver_url(self):
        "Returns the url to upload the project's cases."
        return ' https://www.commcarehq.org/a/%s/receiver' % (self.name)
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
    project = models.ForeignKey(CommCareProject)
    assigned_villages = models.ManyToManyField(Village, through='CommCareUserVillage')
    class Meta:
        unique_together = ("project","username")
    def __unicode__(self):
        return self.username

class CommCareUserVillage(models.Model):
    '''
    This model is used for assigning a user, villages.
    While the ideal mway would have been to include a ManyToManyField in CommCareUser relating to Village,
    this was not possible because Village.id is a BigAutoField and user.id is a AutoField.
    This is a way to simulate ManyToBigManyField.
    '''
    village = BigForeignKey(Village)
    user = models.ForeignKey(CommCareUser)

class CommCareCase(models.Model):
    guid = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    person = BigForeignKey(Person)
    project = models.ForeignKey(CommCareProject)
    user = models.ForeignKey(CommCareUser)
    class Meta:
       unique_together = ("is_open","person","project","user")
       
