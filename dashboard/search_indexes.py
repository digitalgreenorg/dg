import datetime
from haystack.indexes import *
from haystack import site
from dashboard.models import *


class ScreeningIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    location = CharField(model_attr='location')
    date = DateTimeField(model_attr='date')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Screening.objects.all()


site.register(Screening, ScreeningIndex)