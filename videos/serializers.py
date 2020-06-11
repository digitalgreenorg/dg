from rest_framework import serializers
from videos.models import * 
from api.utils import DynamicFieldsModelSerializer

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class VideoSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Video model
    """

    class Meta:
        model = Video
        fields = '__all__'

