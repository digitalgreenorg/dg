from rest_framework import serializers
from geographies.models import Country, State, District, Block, Village
from api.utils import DynamicFieldsModelSerializer

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class CountrySerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Country model
    """

    class Meta:
        model = Country
        fields = '__all__'
    

class StateSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for State model
    """

    country_id = serializers.IntegerField(source='country.id', read_only=True)
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for District model
    """

    country_id = serializers.IntegerField(source='state.country.id', read_only=True)
    country_name = serializers.CharField(source='state.country.country_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    state_name = serializers.CharField(source='state.state_name', read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class BlockSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Block model
    """

    country_id = serializers.IntegerField(source='district.state.country.id', read_only=True)
    country_name = serializers.CharField(source='district.state.country.country_name', read_only=True)
    state_id = serializers.IntegerField(source='district.state.id', read_only=True)
    state_name = serializers.CharField(source='district.state.state_name', read_only=True)
    district_id = serializers.IntegerField(source='district.id', read_only=True)
    district_name = serializers.CharField(source='district.district_name', read_only=True)
    
    class Meta:
        model = Block 
        fields = '__all__'


class VillageSerializer(DynamicFieldsModelSerializer):
    """
    Serializer class inherited from DynamicFieldsModelSerializer for Village model
    """

    country_id = serializers.IntegerField(source='block.district.state.country.id', read_only=True)
    country_name = serializers.CharField(source='block.district.state.country.country_name', read_only=True)
    state_id = serializers.IntegerField(source='block.district.state.id', read_only=True)
    state_name = serializers.CharField(source='block.district.state.state_name', read_only=True)
    district_id = serializers.IntegerField(source='block.district.id', read_only=True)
    district_name = serializers.CharField(source='block.district.district_name', read_only=True)
    block_id = serializers.IntegerField(source='block.id', read_only=True)
    block_name = serializers.CharField(source='block.block_name', read_only=True)
    
    class Meta:
        model = Village 
        fields = '__all__'

        