from django.db import models
Error_list = dict({'SCREENING_SAVE_ERROR'  : -1 ,
                   'SCREENING_READ_ERROR'  : -2 ,                                # Leave blank if you want the error string to be the Exception that was caught
                   'ADOPTION_SAVE_ERROR'   : -3 ,
                   'ADOPTION_READ_ERROR'   : -4 ,
                   'PMA_SAVE_ERROR'        : -5    })


class XMLSubmission(models.Model):
    submission_time = models.DateTimeField(auto_now=True)
    modification_time = models.DateTimeField(auto_now_add=True)
    xml_data = models.TextField()
    error_code = models.IntegerField(null=True)
    error_message = models.TextField(null=True)
