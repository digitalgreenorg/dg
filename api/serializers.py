from rest_framework import serializers
from django.contrib.auth.models import Group
from models import View

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__maintainer__ = "Stuti Verma"
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class ViewSerializer(serializers.Serializer):

    permission_group_id = serializers.CharField(source='permission_groups.id', read_only=True)
    permission_group_name = serializers.CharField(source='permission_groups.name', read_only=True)

    class Meta:
        model = View
        fields = '__all__'


class GroupSerializer(serializers.Serializer):

    class Meta:
        model = Group
        fields = '__all__'
        