# rest framework imports
from rest_framework import serializers
# app imports
from activities.models import Screening
from api.utils import DynamicFieldsModelSerializer

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class ScreeningSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Screening model
    """

    class Meta:
        model = Screening
        fields = '__all__'
