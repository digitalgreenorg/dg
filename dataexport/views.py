from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from forms import *
from activities.models import *
from django.db.models import *
# 
import pandas as pd
import numpy as np
import operator


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
        # viewers_list = PersonMeetingAttendance.objects.filter(screening_id__in=screening_id_list).values('screening_id','person_id').distinct()
        # viewers_list = list(viewers_list)
        # person_id_list = [item.get('person_id') for item in viewers_list]
        # person_gender = list(Person.objects.filter(id__in=person_id_list, gender__in=['M','F']).values('id','gender'))
        # person_gender_map = {}
        # for item in person_gender:
        #     person_gender_map[str(item.get('id'))] = item.get('gender')

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

        return list(data_list)


    # def get_adoption_data(self, date_range, data):
    #     # data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
    #     #                                                 paren)

    def form_valid(self, form):
        cd = form.cleaned_data
        date_range = [cd.get('start_date'), cd.get('end_date')]
        data = int(cd.get('data'))
        data_category = list(cd.get('data_category'))
        if data == 1:
            data_list = self.get_screening_data(date_range, data_category)
        elif data == 2:
            data_list = self.get_adoption_data(date_range, data_category)

        template = "dataexport/table-data.html"
        # data_list = list(data_list)
        # data_list.insert(0, {})
        data = pd.DataFrame(list(data_list))
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
        context = {'data_list': data.to_html()}

        
        return render(self.request, template, context)



class ExportScreening(View):

    def get(self, request, *args, **kwargs):
        template = "dataexport/table-data.html"
        context = {}
        return render(request, template, context)


