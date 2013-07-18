import datetime
from haystack.indexes import *
from haystack import site
from dashboard.models import *


class ScreeningIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    location = CharField(model_attr='location')
    date = DateField(model_attr='date')
    village_id = IntegerField(model_attr='village__id')
    village_name = CharField(model_attr='village__village_name')
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Screening.objects.all()


site.register(Screening, ScreeningIndex)


class CountryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Country.objects.all()

site.register(Country, CountryIndex)

class StateIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return State.objects.all()

site.register(State, StateIndex)

class DistrictIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return District.objects.all()

site.register(District, DistrictIndex)

class BlockIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Block.objects.all()

site.register(Block, BlockIndex)

class VillageIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    id = IntegerField(model_attr='id')
    
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Village.objects.all()

site.register(Village, VillageIndex)
