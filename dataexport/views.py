from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.db.models import *
from django.conf import settings
from django.http import HttpResponse
import pandas as pd
import numpy as np
import operator, ast
import xlsxwriter
import time
import os

from io import BytesIO
from forms import *
from activities.models import *
from dataexport.models import *


class ExportView(FormView):

    template_name = "dataexport/dataexport.html"
    form_class = PageView

    
    def fetch_screening_data(self, date_range, data_category):
        data_list = []
        if data_category == '3': 
            data_list = \
                Screening.objects.filter(date__range=date_range).exclude(farmers_attendance=None\
                                         ).values(
                                         'village_id','partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',\
                                         )
        
        elif data_category == '2':
            data_list = \
                Screening.objects.filter(date__range=date_range).exclude(parentcategory_id=1).exclude(farmers_attendance=None\
                                         ).values(
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',\
                                         )
        elif data_category == '1':
            data_list = \
                Screening.objects.filter(date__range=date_range, parentcategory_id=1).exclude(farmers_attendance=None\
                                         ).values(
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',\
                                         )


        print "Length", len(list(data_list))
        return list(data_list)

    def prepare_data(self):
        # village_list = Village.objects.select_related('block').values('id', 'village_name', 'block_id', 'block__block_name') 
        # block_list = Block.objects.select_related('district').values('block_id', 'block_name', 'district_id', 'district__district_name')
        # district_list = District.objects.select_related('state').values('id', 'district_name', '', 'block__block_name')
        geo_data_list = \
            Village.objects.values('id','village_name','block_id', 'block__block_name','block__district_id',
                                   'block__district__district_name','block__district__state_id',
                                   'block__district__state__state_name','block__district__state__country_id',
                                   'block__district__state__country__country_name')
        geo_frame = pd.DataFrame(list(geo_data_list))
        geo_frame = geo_frame.rename(columns={'id': 'village_id'})
        return geo_frame


    def get_screening_data(self, date_range, data_category):
        category = []
        screening_data = pd.DataFrame(self.fetch_screening_data(date_range, data_category))
        geo_data = self.prepare_data()
        import pdb;pdb.set_trace()
        data_list = pd.merge(geo_data, screening_data, on='village_id')
        
        screening_id_list = data_list['id'].tolist()
        viewers_count_list = \
            PersonMeetingAttendance.objects.filter(screening_id__in=screening_id_list).values('screening_id').annotate(viewer_count=Count('person_id'))

        video_screened = Screening.objects.filter(id__in=screening_id_list).values('id', 'videoes_screened')
        video_title_data_list = Video.objects.values('id', 'title')

        scr_frame = pd.DataFrame(list(video_screened))
        v_frame = pd.DataFrame(list(video_title_data_list))
        v_frame = v_frame.rename(columns={'id': 'videoes_screened'})
        scr_vid_frame = pd.merge(scr_frame, v_frame, on="videoes_screened")

        #hash map of videos and title
        # video_data_dict = {}
        # for item in video_title_data_list:
        #     video_data_dict[item.get('id')]=item.get('title')


        # for item in data_list:
        #     item['video_id'] = []
        #     item['video_title'] = []
            
        #     filtered_data = filter(lambda x: x.get('id') == item.get('id'), video_screened)
        #     for it in filtered_data:
        #         item['video_id'].append(it.get('videoes_screened'))
        #         item['video_title'].append(video_data_dict.get(it.get('videoes_screened')))
 

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
                                state_beneficiary_count_map.get(str(item.get('screening__village__block__district__state__state_name')))[str(_dict.get('id'))] += 1

                    else:
                        for _id in cat:
                            if int(_id) not in person_cat_map.get(str(item.get('person_id'))):
                               person_cat_map[str(item.get('person_id'))].append(int(_id))
                               state_beneficiary_count_map.get(str(item.get('screening__village__block__district__state__state_name')))[str(_id)]+= 1

                else:
                    pass
        except Exception as e:
            print e

        state_beneficiary_count_list = []
        for key, value in state_beneficiary_count_map.items():
            obj = {}
            obj['State'] = key
            obj['Woman of reproductive age (15-49 years)'] = value.get('1')
            obj['Adolescent girl (10-19 years)'] = value.get('2')
            obj['Mother of a child 2 to 5 years'] = value.get('3')
            obj['Mother of a child 6 months to 2 years'] = value.get('4')
            obj['Mother of a child up to 6 months'] = value.get('5')
            obj['Pregnant woman'] = value.get('6')
            state_beneficiary_count_list.append(obj)

        return data_list, state_beneficiary_count_list


    def get_adoption_data(self, date_range, data_category):
        category = []
        if '3' in data_category:
            category = [1,2]
        else:
            category = data_category
        data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range, parentcategory_id__in=category).values('person_id',\
                    'person__person_name','person__gender','video_id','video__title','date_of_adoption','partner_id',\
                    'partner__partner_name','parentcategory_id','parentcategory__parent_category_name',\
                    'adopt_practice','adopt_practice_second','krp_one','krp_two','krp_three',\
                    'krp_four', 'krp_five','person__village__block__district__state__country_id', \
                    'person__village__block__district__state__country__country_name',\
                    'person__village__block__district__state_id','person__village__block__district__state__state_name', \
                    'person__village__block__district_id','person__village__block__district__district_name',\
                    'person__village__block_id','person__village__block__block_name',\
                    'person__village_id','person__village__village_name', 'id')
        data_list = list(data_list)
        return data_list
       

    def form_valid(self, form):
        data = ''
        file_id = None
        cd = form.cleaned_data
        date_range = cd.get('date_period').split(' -')
        date_range = [dte.strip() for dte in date_range]
        data_type = int(cd.get('data'))
        data_category = cd.get('data_category')
        state_beneficiary_count_list = []
        beneficiary_data = []
        data_file = None
        if data_type == 1:
            data_list, state_beneficiary_count_list = self.get_screening_data(date_range, data_category)
        elif data_type == 2:
            data_list = self.get_adoption_data(date_range, data_category)
        if len(data_list):
            table_data_list = data_list[:1000]
            table_data = pd.DataFrame(table_data_list)
            data = pd.DataFrame(data_list)
            if data_type == 1:
                table_data = table_data[['village__block__district__state__country__country_name',\
                              'village__block__district__state__state_name',\
                              'village__block__district__district_name',\
                              'village__block__block_name', 'village__village_name', \
                              'partner__partner_name', 'video_id', 'video_title', 'date', 'parentcategory__parent_category_name',\
                              'id', 'viewer_count']]

                table_data.columns = ['Country Name', 'StateName', \
                                'DistrictName', 'BlockName', 'VillageName',\
                                'PartnerName', 'Video Id', 'Video Title', 'Date', 'Category Name',
                                'Screening#ID',
                                'Viewers Count']
                data = data.rename(columns={'village__block__district__state__country_id':'Country Id',\
                                            'village__block__district__state__country__country_name': 'Country Name',\
                                            'village__block__district__state_id':'State Id',\
                                            'village__block__district__state__state_name':'State Name',\
                                            'village__block__district_id':'District Id',\
                                            'village__block__district__district_name': 'District Name',\
                                            'village__block_id': 'Block Id', 'village__block__block_name': 'Block Name',\
                                            'village_id': 'Village Id', 'village__village_name': 'Village Name',\
                                            'partner_id':'Partner Id', 'partner__partner_name': 'Partner Name',\
                                            'video_id': 'Video Id', 'video_title': 'Video Title', \
                                            'date': 'Date', 'parentcategory_id':'Category', \
                                            'parentcategory__parent_category_name': 'Category Name', \
                                            'id': 'Screening Id', 'viewer_count': 'Viewer Count'})
            else:
                table_data = table_data[['person__village__block__district__state__country__country_name',\
                            'person__village__block__district__state__state_name',\
                            'person__village__block__district__district_name',\
                            'person__village__block__block_name',\
                            'person__village__village_name', 'partner__partner_name','video_id',\
                            'video__title','date_of_adoption','id', 'parentcategory__parent_category_name',\
                            'person_id','person__person_name','person__gender','adopt_practice',\
                            'adopt_practice_second','krp_one','krp_two','krp_three',\
                            'krp_four', 'krp_five']]

                table_data.columns = ['Country Name', 'StateName', \
                                'DistrictName', 'BlockName', 'VillageName',\
                                'PartnerName', 'Video Id', 'Video Title', 'Date of Adoption', 'Adoption ID', 'Category Name',
                                'Person Id','Person Name','Gender','Adopt Practice', 'Adopt Practice 2','Krp 1', 'Krp 2',\
                                'Krp 3','Krp 4', 'Krp 5' 
                                ]
            date_var = datetime.datetime.now()
            filename    = settings.PROJECT_PATH + '/data_file' + '-' + date_var.isoformat()+'.xlsx'
            writer      = pd.ExcelWriter(filename, engine='xlsxwriter')
            data.to_excel(writer, "sheetname")
            writer.save()
            dfile = open(filename, 'r')
            obj, created = TrackFile.objects.get_or_create(name_of_file=dfile.name)    
            file_id = obj.id
            data = table_data.to_html()

        if state_beneficiary_count_list:
            beneficiary_data = pd.DataFrame(state_beneficiary_count_list)
            beneficiary_data = beneficiary_data[['State', 'Woman of reproductive age (15-49 years)',\
                          'Adolescent girl (10-19 years)', 'Mother of a child 2 to 5 years',\
                          'Mother of a child 6 months to 2 years', 'Mother of a child up to 6 months',\
                          'Pregnant woman']]

            beneficiary_data.columns = ['State', 'Woman of reproductive age (15-49 years)',\
                          'Adolescent girl (10-19 years)', 'Mother of a child 2 to 5 years',\
                          'Mother of a child 6 months to 2 years', 'Mother of a child up to 6 months',\
                          'Pregnant woman']
            beneficiary_data = beneficiary_data.to_html()


        context = {'data_list': data, 'beneficiary_data_list': beneficiary_data, 
                   'start_date': cd.get('start_date'), 'end_date': cd.get('end_date'),
                   'file_id': file_id}
        template = "dataexport/table-data.html"
        return render(self.request, template, context)



class DownloadFile(View):

    def get(self, request, *args, **kwargs):
        file_path = TrackFile.objects.get(id=kwargs.get('file_id')).name_of_file
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


