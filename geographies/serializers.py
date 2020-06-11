from .models import * 
from rest_framework import serializers

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__maintainer__ = "Stuti Verma"
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CountrySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
    

class StateSerializer(DynamicFieldsModelSerializer):
    country_id = serializers.IntegerField(source='country.id', read_only=True)
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    
    class Meta:
        model = State
        fields = '__all__'


class DistrictSerializer(DynamicFieldsModelSerializer):
    country_id = serializers.IntegerField(source='state.country.id', read_only=True)
    country_name = serializers.CharField(source='state.country.country_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    state_name = serializers.CharField(source='state.state_name', read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class BlockSerializer(DynamicFieldsModelSerializer):
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

        