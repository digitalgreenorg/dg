from programs.models import *
from rest_framework import serializers
from api.utils import DynamicFieldsModelSerializer

class PartnerSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Partner model
    """

    class Meta:
        model = Partner
        fields = '__all__'


class ProjectSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Project model
    """

    class Meta:
        model = Project
        fields = '__all__'

        