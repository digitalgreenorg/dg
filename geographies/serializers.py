from .models import * 
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'old_coco_id','country_name','start_date', 'active']
    
class StateSerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(source='country.id', read_only=True)
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    class Meta:
        model = State
        fields = ['id','old_coco_id','state_name','country_id','country_name','start_date', 'active']

class DistrictSerializer(serializers.ModelSerializer):
    country_id = serializers.IntegerField(source='state.country.id', read_only=True)
    country_name = serializers.CharField(source='state.country.country_name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)
    state_name = serializers.CharField(source='state.state_name', read_only=True)
    class Meta:
        model = District
        fields = ['id','old_coco_id','district_name','start_date','state_id','state_name','country_id','country_name','latitude', 'longitude', 'active']


class BlockSerializer(serializers.ModelSerializer):
    # country_id = serializers.IntegerField(source='district.state.country.id', read_only=True)
    # country_name = serializers.CharField(source='district.state.country.country_name', read_only=True)
    # state_id = serializers.IntegerField(source='district.state.id', read_only=True)
    # state_name = serializers.CharField(source='district.state.state_name', read_only=True)
    # district_id = serializers.IntegerField(source='district.id', read_only=True)
    # district_name = serializers.CharField(source='district.district_name', read_only=True)
    class Meta:
        model = Block #'district_id','district_name', 'state_id','state_name','country_id','country_name',
        fields = ['id','old_coco_id','block_name', 'start_date','latitude', 'longitude']


class VillageSerializer(serializers.ModelSerializer):
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
        fields = ['id','old_coco_id','village_name','block_id','block_name','district_id','district_name','start_date','state_id','state_name','country_id','country_name','latitude', 'longitude', 'grade','active']
