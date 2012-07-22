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