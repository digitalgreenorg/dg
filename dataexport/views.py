from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from forms import *
from activities.models import *
from django.db.models import *
# 
import pandas as pd
import numpy as np
import operator, ast


class ExportView(FormView):

    template_name = "dataexport/dataexport.html"
    form_class = PageView

    def get_screening_data(self, date_range, data_category):
        data_list = Screening.objects.filter(date__range=date_range, 
                                             parentcategory_id__range=[1,3]).exclude(farmers_attendance=None).values('village__block__district__state__country_id',\
                                             'village__block__district__state__country__country_name', \
                                             'village__block__district__state_id', 'village__block__district__state__state_name', \
                                             'village__block__district_id', 'village__block__district__district_name', \
                                             'village__block_id', 'village__block__block_name', \
                                             'village_id', 'village__village_name', 'partner_id', 'partner__partner_name',\
                                             'date',\
                                             'parentcategory_id',\
                                             'parentcategory__parent_category_name','id',\

                                             )

        data_list = list(data_list)
        screening_id_list = [item.get('id') for item in data_list]
        viewers_count_list = PersonMeetingAttendance.objects.filter(screening_id__in=screening_id_list).values('screening_id').annotate(viewer_count=Count('person_id'))

        for item in data_list:
            try:
                screening_obj = Screening.objects.get(pk=item.get('id'))
                video_screened_obj = screening_obj.videoes_screened.all().values('id','title')                
                item['video_id'] = ''
                item['video_title'] = ''
                for video in video_screened_obj:
                    item['video_id'] += str(video.get('id')) + ' , '
                    item['video_title'] += video.get('title') + ' , '

            except Exception as e:
                print e

        for item in viewers_count_list:
            item['id'] = item.get('screening_id')
            del item['screening_id']
        

        sorting_key = operator.itemgetter('id')    
        for i, j in zip(sorted(data_list, key = sorting_key), sorted(viewers_count_list, key = sorting_key)):
            i.update(j)


        '''Beneficiary Data State Wise'''
        state_beneficiary_count_map = {}
        person_cat_map = {}
        queryset = list(PersonMeetingAttendance.objects.filter(screening__date__range=date_range).select_related('screening').values('screening__village__block__district__state__state_name','person_id','category'))
        try:
            for item in queryset:
                if state_beneficiary_count_map.get(str(item.get('screening__village__block__district__state__state_name'))) is None:
                    state_beneficiary_count_map[str(item.get('screening__village__block__district__state__state_name'))] = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0}

                if item.get('category') is not None:
                    if person_cat_map.get(str(item.get('person_id'))) is None:
                        person_cat_map[str(item.get('person_id'))] = []
                    cat = ast.literal_eval(item.get('category'))
                    if isinstance(cat[0], dict):
                        for _dict in cat:
                            if int(_dict.get('id')) not in person_cat_map.get(str(item.get('person_id'))):
                                person_cat_map[str(item.get('person_id'))].append(int(_dict.get('id')))
                                state_beneficiary_count_map.get(str(item.get('screening__village__block__district__state__state_name'))).get(str(_dict.get('id'))) += 1

                    else:
                        for _id in cat:
                            if int(_id) not in person_cat_map.get(str(item.get('person_id'))):
                               person_cat_map[str(item.get('person_id'))].append(int(_id))
                               state_beneficiary_count_map.get(str(item.get('screening__village__block__district__state__state_name'))).get(str(_id)) += 1

                else:
                    pass
        except Exception as e:
            print e

        return data_list


    # def get_adoption_data(self, date_range, data):
    #     # data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
    #     #                                                 paren)

    def form_valid(self, form):
        data = ''
        cd = form.cleaned_data
        date_range = [cd.get('start_date'), cd.get('end_date')]
        data = int(cd.get('data'))
        data_category = list(cd.get('data_category'))
        if data == 1:
            data_list = self.get_screening_data(date_range, data_category)
        elif data == 2:
            data_list = self.get_adoption_data(date_range, data_category)
        if len(data_list):

            data = pd.DataFrame(data_list)
            data = data[['village__block__district__state__country_id', 'village__block__district__state__country__country_name',\
                          'village__block__district__state_id', 'village__block__district__state__state_name',\
                          'village__block__district_id', 'village__block__district__district_name',\
                          'village__block_id', 'village__block__block_name', 'village_id', 'village__village_name', \
                          'partner_id', 'partner__partner_name', 'video_id', 'video_title', 'date', 'parentcategory_id', 'parentcategory__parent_category_name',\
                          'id', 'viewer_count']]
            data.columns = ['CountryID', 'Country Name', 'StateID', "StateName", 'DistrictID', \
                            'DistrictName', 'BlockId', 'BlockName', 'VillageID', 'VillageName',\
                            'Partner ID', 'PartnerName', 'Video Id', 'Video Title', 'Date', 'Category ID', 'Category Name',
                            'Screening#ID',
                            'Viewers Count']
            data = data.to_html()

        context = {'data_list': data, 'start_date': cd.get('start_date'), 'end_date': cd.get('end_date')}
        template = "dataexport/table-data.html"
        return render(self.request, template, context)



class ExportScreening(View):

    def get(self, request, *args, **kwargs):
        template = "dataexport/table-data.html"
        context = {}
        return render(request, template, context)


