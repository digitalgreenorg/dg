from people.models import Person
from rest_framework import serializers
from geographies.models import Village, Block, District, State, Country
from geographies.serializers import VillageSerializer
from api.utils import DynamicFieldsModelSerializer

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class FarmerSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Village model
    """

    village_id = serializers.CharField(source='village.id', read_only=True)
    village = serializers.CharField(source='village.village_name', read_only=True)

    block_id = serializers.IntegerField(source='village.block.id', read_only=True)
    block_name = serializers.CharField(source='village.block.block_name', read_only=True)

    district_id = serializers.IntegerField(source='village.block.district.id', read_only=True)
    district_name = serializers.CharField(source='village.block.district.district_name', read_only=True)

    state_id = serializers.IntegerField(source='village.block.district.state.id', read_only=True)
    state_name = serializers.CharField(source='village.block.district.state.state_name', read_only=True)
    
    country_id = serializers.IntegerField(source='village.block.district.state.country.id', read_only=True)
    country_name = serializers.CharField(source='village.block.district.state.country.country_name', read_only=True)

    class Meta:
        model = Person 
        fields = '__all__'
    
