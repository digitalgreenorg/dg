from django.db import models

from dashboard.models import Person
from dashboard.fields import BigAutoField


MIN_ONLINE = 10000000000000
# Minimum possible Offline ID for user: path_rae_bareilly
MIN_OFFLINE_PRB = 68000000000
MAX_OFFLINE_PRB = 69000000000

# Id for district Rae Bareilly
DISTRICT_ID = 10000000000041
spreadsheet_key = '0AsotIQD30kd_dGZXZEZiVE9nYlhvNURPSXNSdFM2RGc'
worksheet_id = 'od6'

class PathLog(models.Model):
    id = BigAutoField(primary_key = True)
    person_offline_id = models.BigIntegerField()
    person_online_id = models.BigIntegerField()
    read = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=False,auto_now_add=True)
    read_time = models.DateTimeField(auto_now=True,auto_now_add=False)
    
