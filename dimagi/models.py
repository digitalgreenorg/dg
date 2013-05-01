from django.db import models
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
    username = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_code = models.IntegerField(null=True)
    error_message = models.TextField(null=True)
    