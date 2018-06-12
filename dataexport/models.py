from django.db import models
from coco.base_models import CocoModel

# Create your models here.

class TrackFile(CocoModel):
	name_of_file = models.TextField(null=True)

