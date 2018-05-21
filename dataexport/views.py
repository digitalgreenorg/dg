from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from forms import *
from activities.models import *
# 
import pandas as pd
import numpy as np


class ExportView(FormView):

    template_name = "dataexport/dataexport.html"
    form_class = PageView

    def get_screening_data(self, date_range, data):
        data_list = Screening.objects.filter(date__range=date_range, 
                                             parentcategory_id=1).values('village_id', \
                                             'village__village_name', 'date',\
                                             'parentcategory__parent_category_name')
        import pdb;pdb.set_trace()
        return list(data_list)

    def form_valid(self, form):
        cd = form.cleaned_data
        date_range = [cd.get('start_date'), cd.get('end_date')]
        data = int(cd.get('data'))
        data_category = cd.get('data_category')
        if data == 1:
            # call screening data
            data_list = self.get_screening_data(date_range, data)
        template = "dataexport/table-data.html"
        context = {'data_list': pd.DataFrame(list(data_list)).to_html()}
        return render(self.request, template, context)



class ExportScreening(View):

    def get(self, request, *args, **kwargs):
        template = "dataexport/table-data.html"
        context = {}
        return render(request, template, context)


