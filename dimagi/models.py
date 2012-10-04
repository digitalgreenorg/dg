from django.db import models
Error_list = {}
Error_list [-1] = 'SCREEENING_SAVE_ERROR'
Error_list [-2] = 'SCREEENING_REAS_ERROR'                                # Leave blank if you want the error string to be the Exception that was caught
Error_list [-3] = 'ADOPTION_SAVE_ERROR'
Error_list [-4] = 'ADOPTION_READ_ERROR'
Error_list [-5] = 'PMA_SAVE_ERROR'

class XMLSubmission(models.Model):
    submission_time = models.DateTimeField(auto_now=True)
    modification_time = models.DateTimeField(auto_now_add=True)
    xml_data = models.TextField()
    error_code = models.IntegerField()
    error_message = models.TextField()
