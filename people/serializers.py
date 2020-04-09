from people.models import Person
from rest_framework import serializers
from geographies.models import Village


class VillageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Village
        fields = ['id', 'village_name']


class FarmerSerializer(serializers.ModelSerializer):

    village_id = serializers.CharField(source='village.id', read_only=True)
    village_name = serializers.CharField(source='village.village_name', read_only=True)

    class Meta:
        model = Person
        fields = ['person_name', 'phone_no', 'gender', 'village_id','village_name']

