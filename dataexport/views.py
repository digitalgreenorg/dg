from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.db.models import *
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.db.models import Count, Min, Sum, Avg, Max, F

import ast
import os
import pandas as pd
from dataexport.forms import *
from activities.models import *
from dataexport.models import *
import datetime


class ExportView(FormView):

    template_name = "dataexport/dataexport.html"
    form_class = PageView


    def get(self, request):
        todays_date = datetime.datetime.now().strftime('%Y-%m-%d')
        year_ago_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        total_screenings = Screening.objects.filter(date__range=[year_ago_date, todays_date]).count();
        total_adoptions = PersonAdoptPractice.objects.filter(date_of_adoption__range=[year_ago_date, todays_date]).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
        total_unique_viewers = PersonMeetingAttendance.objects.filter(screening__date__range=[year_ago_date, todays_date]).aggregate(unique_viewers=Count('person_id', distinct=True))
        context = {'total_screenings': total_screenings, 'total_adoptions' : total_adoptions.get('adoptions'), \
                    'total_viewers': total_unique_viewers.get('unique_viewers'), \
                    'total_unique_adopters': total_adoptions.get('unique_adopters'),\
                    'form': self.form_class}
        
        return render(request, self.template_name, context)
    
    def fetch_screening_data(self, date_range, data_category, country, state):
        data_list = []
        if data_category == '3' and len(state): 
            data_list = \
                Screening.objects.filter(date__range=date_range,
                                         village__block__district__state__country_id=country.id,
                                         village__block__district__state_id__in=state).values( \
                                         'village_id','partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )

        elif data_category == '3':
            data_list = \
                Screening.objects.filter(date__range=date_range,
                                         village__block__district__state__country_id=country.id
                                         ).values( \
                                         'village_id','partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )
        
        elif data_category == '2' and len(state):
            data_list = \
                Screening.objects.filter(date__range=date_range,
                                         village__block__district__state__country_id=country.id,
                                         village__block__district__state_id__in=state).exclude(parentcategory_id=1)\
                                         .values(\
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )
        elif data_category == '2':
            data_list = \
                Screening.objects.filter(date__range=date_range,
                                         village__block__district__state__country_id=country.id
                                         ).exclude(parentcategory_id=1).values( \
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )
        elif data_category == '1' and len(state):
            data_list = \
                Screening.objects.filter(date__range=date_range, parentcategory_id=data_category,
                                         village__block__district__state__country_id=country.id,
                                         village__block__district__state_id__in=state
                                         ).values( \
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )
        elif data_category == '1':
            data_list = \
                Screening.objects.filter(date__range=date_range, parentcategory_id=data_category,
                                         village__block__district__state__country_id=country.id,
                                         ).values( \
                                         'village_id', 'partner_id', 'partner__partner_name',\
                                         'date',\
                                         'parentcategory_id',\
                                         'parentcategory__parent_category_name','id',
                                         'time_created'
                                         )


        return list(data_list)

    def prepare_data(self):
        # geo query
        geo_data_list = \
            Village.objects.values('id','village_name','block_id', 'block__block_name','block__district_id',
                                   'block__district__district_name','block__district__state_id',
                                   'block__district__state__state_name','block__district__state__country_id',
                                   'block__district__state__country__country_name')
        # converting to geo frame
        geo_frame = pd.DataFrame(list(geo_data_list))
        # renaming geo_frame columns
        geo_frame = geo_frame.rename(columns={'id': 'village_id'})
        return geo_frame


    def get_screening_data(self, date_range, data_category, country, state):
        # defining containers
        category = []
        data_list_to_be_rendered = []
        data_list_rendered = []
        state_beneficiary_count_list = []
        district_reach_frame = []
        # calling the screening data and converting it to data frame
        screening_data = pd.DataFrame(self.fetch_screening_data(date_range, data_category, country, state))
        # calling the gep frame data
        geo_data = self.prepare_data()
        if len(screening_data):
            # first merging the screening frame with geo frame. This will append geo columns
            data_list = pd.merge(geo_data, screening_data, on='village_id')
            # collecting all screening id and fetch its attendance
            screening_id_list = data_list['id'].tolist()
            # fetching the attendance based on screening id obtained above.
            viewers_count_list = \
                PersonMeetingAttendance.objects.filter(screening_id__in=screening_id_list).values('screening_id').annotate(viewer_count=Count('person_id'))
### 86570

            #import pdb; pdb.set_trace()
            viewers_count_list_AP=\
                   AP_Screening.objects.filter(screening_id__in=screening_id_list).values('screening_id','total_members')
            # unique viewers district wise
            if len(state):
                district_reach_queryset = list(PersonMeetingAttendance.objects.filter(screening__village__block__district__state_id__in=state, screening__date__range=date_range\
                    ).select_related('screening').values('screening__village__block__district_id', 'screening__village__block__district__district_name').annotate(unique_viewers=Count('person_id',distinct=True)))
            else:
                district_reach_queryset = list(PersonMeetingAttendance.objects.filter(screening__date__range=date_range\
                    ).select_related('screening').values('screening__village__block__district_id', 'screening__village__block__district__district_name').annotate(unique_viewers=Count('person_id',distinct=True)))
            district_reach_frame = pd.DataFrame(district_reach_queryset)
            district_reach_frame = district_reach_frame.rename(columns={'screening__village__block__district_id': 'District ID',
                                                                        'screening__village__block__district__district_name':
                                                                        'District Name',
                                                                        'unique_viewers': 'Reach'})
            
            # get all videos screening from the list of screening ids. At this point we are sure
            # about screening ids and hence we are fetching its related videos.
            video_screened = Screening.objects.filter(id__in=screening_id_list).values('id', 'videoes_screened')
            # converting it to data frame.
           
            scr_frame = pd.DataFrame(list(video_screened))
            # fetching and making the video data set first
            video_title_data_list = Video.objects.values('id', 'title')
            # converting the video data set into frames
            v_frame = pd.DataFrame(list(video_title_data_list))
            # renaming the column to preapre for merge
            v_frame = v_frame.rename(columns={'id': 'videoes_screened'})
            # merging the videos id with name to complete data set
            scr_vid_frame = pd.merge(scr_frame, v_frame, on="videoes_screened")
            # merging screening frame with video-screening frame to append video data.
            # at this point we have merged geo-scr frame and video-scr frame.
            data_list_to_be_rendered = pd.merge(data_list, scr_vid_frame, on="id")
            # creating the viewers frame.
            viewers_frame = pd.DataFrame(list(viewers_count_list))
            viewers_frame_AP = pd.DataFrame(list(viewers_count_list_AP))

            # renaming the column for viewers frame.
            viewers_frame = viewers_frame.rename(columns={'screening_id': 'id'})
            viewers_frame_AP = viewers_frame_AP.rename(columns={'screening_id': 'id'})
            viewers_frame_AP = viewers_frame_AP.rename(columns={'total_members': 'viewer_count'})

            viewers_frame_final=viewers_frame.append(viewers_frame_AP)
            
            # finally merging the viewers frame.
            data_list_rendered = pd.merge(data_list_to_be_rendered, viewers_frame_final, on="id")
            
           ### import pdb; pdb.set_trace()
            # Beneficiary Data State Wise
            state_beneficiary_count_map = {}
            person_cat_map = {}
            if not len(state):
                queryset = list(PersonMeetingAttendance.objects.filter(screening__date__range=date_range,
                        screening__village__block__district__state__country_id=country.id,
                        ).select_related('screening').values('screening__village__block__district__state__state_name','person_id','category'))
            else:
                queryset = list(PersonMeetingAttendance.objects.filter(screening__date__range=date_range,
                        screening__village__block__district__state_id__in=state,
                        ).select_related('screening').values('screening__village__block__district__state__state_name','person_id','category'))
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

        if isinstance(data_list_rendered, list):
            data_list_rendered = pd.DataFrame(data_list_rendered)
        return {'data_list_rendered': data_list_rendered, 'state_beneficiary_count_list': state_beneficiary_count_list,
                'district_reach': district_reach_frame}


    def get_adoption_data(self, date_range, data_category, country, state):
        category = []
        if '3' in data_category and len(state):
            category = [1,2]
            data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
                                                       person__village__block__district__state__country_id=country.id,
                                                       person__village__block__district__state_id__in=state).values('person_id',\
                    'person__person_name','person__gender','person__phone_no', 'video_id','video__title','date_of_adoption','partner_id',\
                    'partner__partner_name','parentcategory_id','parentcategory__parent_category_name',\
                    'adopt_practice','adopt_practice_second','krp_one','krp_two','krp_three',\
                    'krp_four', 'krp_five','person__village__block__district__state__country_id', \
                    'person__village__block__district__state__country__country_name',\
                    'person__village__block__district__state_id','person__village__block__district__state__state_name', \
                    'person__village__block__district_id','person__village__block__district__district_name',\
                    'person__village__block_id','person__village__block__block_name',\
                    'person__village_id','person__village__village_name', 'id', 'time_created')
        elif '3' in data_category:
            category = [1,2]
            data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
                                                       person__village__block__district__state__country_id=country.id,
                                                       ).values('person_id',\
                    'person__person_name','person__gender','person__phone_no', 'video_id','video__title','date_of_adoption','partner_id',\
                    'partner__partner_name','parentcategory_id','parentcategory__parent_category_name',\
                    'adopt_practice','adopt_practice_second','krp_one','krp_two','krp_three',\
                    'krp_four', 'krp_five','person__village__block__district__state__country_id', \
                    'person__village__block__district__state__country__country_name',\
                    'person__village__block__district__state_id','person__village__block__district__state__state_name', \
                    'person__village__block__district_id','person__village__block__district__district_name',\
                    'person__village__block_id','person__village__block__block_name',\
                    'person__village_id','person__village__village_name', 'id', 'time_created')


        else:
            category = data_category
            if len(state):
                data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
                                                       person__village__block__district__state__country_id=country.id,
                                                       person__village__block__district__state_id__in=state).values('person_id',\
                    'person__person_name','person__gender','person__phone_no', 'video_id','video__title','date_of_adoption','partner_id',\
                    'partner__partner_name','parentcategory_id','parentcategory__parent_category_name',\
                    'adopt_practice','adopt_practice_second','krp_one','krp_two','krp_three',\
                    'krp_four', 'krp_five','person__village__block__district__state__country_id', \
                    'person__village__block__district__state__country__country_name',\
                    'person__village__block__district__state_id','person__village__block__district__state__state_name', \
                    'person__village__block__district_id','person__village__block__district__district_name',\
                    'person__village__block_id','person__village__block__block_name',\
                    'person__village_id','person__village__village_name', 'id', 'time_created')
                if category == '2':
                    data_list = data_list.exclude(parentcategory_id=1)
                else:
                    data_list = data_list.filter(parentcategory_id=1)
            else:
                data_list = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range,
                                                       person__village__block__district__state__country_id=country.id,
                                                       ).values('person_id',\
                    'person__person_name','person__gender','person__phone_no', 'video_id','video__title','date_of_adoption','partner_id',\
                    'partner__partner_name','parentcategory_id','parentcategory__parent_category_name',\
                    'adopt_practice','adopt_practice_second','krp_one','krp_two','krp_three',\
                    'krp_four', 'krp_five','person__village__block__district__state__country_id', \
                    'person__village__block__district__state__country__country_name',\
                    'person__village__block__district__state_id','person__village__block__district__state__state_name', \
                    'person__village__block__district_id','person__village__block__district__district_name',\
                    'person__village__block_id','person__village__block__block_name',\
                    'person__village_id','person__village__village_name', 'id', 'time_created')
                if category == '2':
                    data_list = data_list.exclude(parentcategory_id=1)
                else:
                    data_list = data_list.filter(parentcategory_id=1)
        
        data_list = pd.DataFrame(list(data_list))
        return data_list
       
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
      return super(ExportView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        data = ''
        table_data_count = 0
        data_list_count = 0
        district_reach = 0
        file_id = None
        table_data = []
        cd = form.cleaned_data
        date_range = cd.get('date_period').split(' -')
        date_range = [dte.strip() for dte in date_range]
        data_type = int(cd.get('data'))
        data_category = cd.get('data_category')
        country = cd.get('country')
        state= self.request.POST.getlist('state')
        state_beneficiary_count_list = []
        beneficiary_data = []
        data_file = None
        category = []
        if '3' in data_category and len(state):
            category = [1,2]
            total_screenings = Screening.objects.filter(date__range=date_range, \
                                village__block__district__state_id__in=state).count()
                                
            total_adoptions = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range, \
                                person__village__block__district__state_id__in=state).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
            total_unique_viewers = PersonMeetingAttendance.objects.filter(screening__date__range=date_range, \
                                screening__village__block__district__state_id__in=state).aggregate(unique_viewers=Count('person_id', distinct=True))
        elif '3' in data_category:
            category = [1,2]
            total_screenings = Screening.objects.filter(date__range=date_range, \
                                village__block__district__state__country_id=country.id).count()
            total_adoptions = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range, \
                                person__village__block__district__state__country_id=country.id).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
            total_unique_viewers = PersonMeetingAttendance.objects.filter(screening__date__range=date_range,\
                                screening__village__block__district__state__country_id=country.id).aggregate(unique_viewers=Count('person_id', distinct=True))

        else:
            category = data_category
            if len(state):
                total_screenings = Screening.objects.filter(date__range=date_range, \
                                village__block__district__state_id__in=state)
                total_adoptions = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range, \
                                    person__village__block__district__state_id__in=state)
                total_unique_viewers = PersonMeetingAttendance.objects.filter(screening__date__range=date_range, \
                                    screening__village__block__district__state_id__in=state) 
                if category == '2':
                    total_screenings = total_screenings.exclude(parentcategory_id=1).count()
                    total_adoptions = total_adoptions.exclude(parentcategory_id=1).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
                    total_unique_viewers = total_unique_viewers.exclude(screening__parentcategory_id=1).aggregate(unique_viewers=Count('person_id', distinct=True))
                else:
                    total_screenings = total_screenings.filter(parentcategory_id=1).count()
                    total_adoptions = total_adoptions.filter(parentcategory_id=1).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
                    total_unique_viewers = total_unique_viewers.filter(screening__parentcategory_id=1).aggregate(unique_viewers=Count('person_id', distinct=True))   
            
            else:
                total_screenings = Screening.objects.filter(date__range=date_range,\
                                    village__block__district__state__country_id=country.id)
                total_adoptions = PersonAdoptPractice.objects.filter(date_of_adoption__range=date_range, \
                                    person__village__block__district__state__country_id=country.id)
                total_unique_viewers = PersonMeetingAttendance.objects.filter(screening__date__range=date_range, \
                                    screening__village__block__district__state__country_id=country.id)
                if category == '2':
                    total_screenings = total_screenings.exclude(parentcategory_id=1).count()
                    total_adoptions = total_adoptions.exclude(parentcategory_id=1).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
                    total_unique_viewers = total_unique_viewers.exclude(screening__parentcategory_id=1).aggregate(unique_viewers=Count('person_id', distinct=True))
                else:
                    total_screenings = total_screenings.filter(parentcategory_id=1).count()
                    total_adoptions = total_adoptions.filter(parentcategory_id=1).aggregate(adoptions=Count('id'), unique_adopters=Count('person_id', distinct=True))
                    total_unique_viewers = total_unique_viewers.filter(screening__parentcategory_id=1).aggregate(unique_viewers=Count('person_id', distinct=True))
 
        if data_type == 1:
            # fetching the screening data
            screening_dict = self.get_screening_data(date_range, data_category, country, state)
            data_list = screening_dict.get('data_list_rendered')
            state_beneficiary_count_list = screening_dict.get('state_beneficiary_count_list')
            district_reach = screening_dict.get('district_reach')
            if len(district_reach):
                district_reach= district_reach.to_html(index=False)


        elif data_type == 2:
            # fetching the adoption data
            data_list = self.get_adoption_data(date_range, data_category, country, state)
        # checking whether the data list frame is not empty.
        if not data_list.empty:
            # preparing the table data
            table_data_list = data_list[:1000]
            # converting the sliced data into data frame
            table_data = pd.DataFrame(table_data_list)
            data = pd.DataFrame(data_list)
            if data_type == 1:
                # ordering of columns
                data = data[['block__district__state__country_id',
                             'block__district__state__country__country_name',
                             'block__district__state_id',
                             'block__district__state__state_name',
                             'block__district_id',
                             'block__district__district_name',
                             'block_id',
                             'block__block_name',
                             'village_id',
                             'village_name',
                             'partner_id',
                             'partner__partner_name',
                             'videoes_screened',
                             'title',
                             'date',
                             'time_created',
                             'parentcategory_id',
                             'parentcategory__parent_category_name',
                             'id',
                             'viewer_count']]
                data = data.rename(columns={'block__district__state__country_id':'Country Id',\
                                            'block__district__state__country__country_name': 'Country Name',\
                                            'block__district__state_id':'State Id',\
                                            'block__district__state__state_name':'State Name',\
                                            'block__district_id':'District Id',\
                                            'block__district__district_name': 'District Name',\
                                            'block_id': 'Block Id', 'block__block_name': 'Block Name',\
                                            'village_id': 'Village Id', 'village_name': 'Village Name',\
                                            'partner_id':'Partner Id', 'partner__partner_name': 'Partner Name',\
                                            'videoes_screened': 'Video Id', 'title': 'Video Title', \
                                            'date': 'Date', 
                                            'time_created': 'System Date',
                                            'parentcategory_id':'Category #ID', \
                                            'parentcategory__parent_category_name': 'Category Name', \
                                            'id': 'Screening Id', 'viewer_count': 'Viewer Count'})
            else:
                #Checking fields for Odisha(H&N)
                if '3' in state:
                    data = data[['person__village__block__district__state__country_id',
                                 'person__village__block__district__state__country__country_name',
                                 'person__village__block__district__state_id',
                                 'person__village__block__district__state__state_name',
                                 'person__village__block__district_id',
                                 'person__village__block__district__district_name',
                                 'person__village__block_id',
                                 'person__village__block__block_name',
                                 'person__village_id',
                                 'person__village__village_name',
                                 'partner_id',
                                 'partner__partner_name',
                                 'video_id',
                                 'video__title',
                                 'date_of_adoption',
                                 'time_created',
                                 'id',
                                 'parentcategory__parent_category_name',
                                 'person_id',
                                 'person__person_name',
                                 'person__gender',
                                 'person__phone_no',
                                 'adopt_practice',
                                 'adopt_practice_second',
                                 'krp_one',
                                 'krp_two',
                                 'krp_three',
                                 'krp_four',
                                 'krp_five'
                                 ]]

                    data = data.rename(columns={'person__village__block__district__state__country_id': 'Country #ID',
                                       'person__village__block__district__state__country__country_name': 'Country Name',
                                       'person__village__block__district__state_id': 'State #ID',
                                       'person__village__block__district__state__state_name': 'State Name',
                                       'person__village__block__district_id': 'District #ID',
                                       'person__village__block__district__district_name': 'District Name',
                                       'person__village__block_id': 'Block #ID',
                                       'person__village__block__block_name': 'Block Name',
                                       'person__village_id': 'Village #ID',
                                       'person__village__village_name': 'Village Name',
                                       'partner_id': 'Partner #ID',
                                       'partner__partner_name': 'Partner Name',
                                       'video_id': 'Video #ID',
                                       'video__title':'Video Title',
                                       'date_of_adoption': 'Date of Adoption',
                                       'time_created': 'System Date',
                                       'id': 'Adoption #ID',
                                       'parentcategory__parent_category_name': 'Parent Category Name',
                                       'person_id': 'Person #ID',
                                       'person__person_name': 'Person Name',
                                       'person__gender': 'Gender',
                                       'person__phone_no': 'Phone Number',
                                       'adopt_practice': 'Adopt Practice',
                                       'adopt_practice_second': 'Adopt Practice 2',
                                       'krp_one': 'KRP1',
                                       'krp_two': 'KRP2',
                                       'krp_three': 'KRP3',
                                       'krp_four': 'KRP4',
                                       'krp_five': 'KRP5'})
                else:
                    data = data[['person__village__block__district__state__country_id',
                                 'person__village__block__district__state__country__country_name',
                                 'person__village__block__district__state_id',
                                 'person__village__block__district__state__state_name',
                                 'person__village__block__district_id',
                                 'person__village__block__district__district_name',
                                 'person__village__block_id',
                                 'person__village__block__block_name',
                                 'person__village_id',
                                 'person__village__village_name',
                                 'partner_id',
                                 'partner__partner_name',
                                 'video_id',
                                 'video__title',
                                 'date_of_adoption',
                                 'time_created',
                                 'id',
                                 'parentcategory__parent_category_name',
                                 'person_id',
                                 'person__person_name',
                                 'person__gender',
                                 'person__phone_no',
                                 'adopt_practice'
                                 ]]

                    data = data.rename(columns={'person__village__block__district__state__country_id': 'Country #ID',
                                       'person__village__block__district__state__country__country_name': 'Country Name',
                                       'person__village__block__district__state_id': 'State #ID',
                                       'person__village__block__district__state__state_name': 'State Name',
                                       'person__village__block__district_id': 'District #ID',
                                       'person__village__block__district__district_name': 'District Name',
                                       'person__village__block_id': 'Block #ID',
                                       'person__village__block__block_name': 'Block Name',
                                       'person__village_id': 'Village #ID',
                                       'person__village__village_name': 'Village Name',
                                       'partner_id': 'Partner #ID',
                                       'partner__partner_name': 'Partner Name',
                                       'video_id': 'Video #ID',
                                       'video__title':'Video Title',
                                       'date_of_adoption': 'Date of Adoption',
                                       'time_created': 'System Date',
                                       'id': 'Adoption #ID',
                                       'parentcategory__parent_category_name': 'Parent Category Name',
                                       'person_id': 'Person #ID',
                                       'person__person_name': 'Person Name',
                                       'person__gender': 'Gender',
                                       'person__phone_no': 'Phone Number',
                                       'adopt_practice': 'Adopt Practice'
                                       })


            data_list_count = len(data)
            # for displying the table data we require less number of columns
            if data_type == 1:
                # for screening we are specifying what columns we are displaying.
                table_data = table_data[['block__district__district_name','block__block_name', 'village_name','partner__partner_name', 'videoes_screened', 'title', 'date', 'parentcategory__parent_category_name','id', 'viewer_count']]
                table_data.columns = [
                                        'DistrictName', 'BlockName', 'VillageName',\
                                        'PartnerName', 'Video Id', 'Video Title', 'Date', 'Category Name',
                                        'Screening#ID',
                                        'Viewers Count']
                # for screening we are renaming the columns
                data = data.rename(columns={'block__district__state__country_id':'Country Id',\
                                        'block__district__state__country__country_name': 'Country Name',\
                                        'block__district__state_id':'State Id',\
                                        'block__district__state__state_name':'State Name',\
                                        'block__district_id':'District Id',\
                                        'block__district__district_name': 'District Name',\
                                        'block_id': 'Block Id', 'block__block_name': 'Block Name',\
                                        'village_id': 'Village Id', 'village__village_name': 'Village Name',\
                                        'partner_id':'Partner Id', 'partner__partner_name': 'Partner Name',\
                                        'videoes_screened': 'Video Id', 'title': 'Video Title', \
                                        'date': 'Date', 'parentcategory_id':'Category', \
                                        'parentcategory__parent_category_name': 'Category Name', \
                                        'id': 'Screening Id', 'viewer_count': 'Viewer Count'})
            else:
                # for adoption we are specifying what columns we are displaying.
                table_data = table_data[['person__village__block__district__state__country__country_name',\
                            'person__village__block__district__state__state_name',\
                            'person__village__block__district__district_name',\
                            'person__village__block__block_name',\
                            'person__village__village_name', 'partner__partner_name',\
                            'video__title','date_of_adoption', 'parentcategory__parent_category_name',\
                            'person__person_name','person__gender']]

                table_data.columns = ['Country Name', 'StateName', \
                                'DistrictName', 'BlockName', 'VillageName',\
                                'PartnerName', 'Video Title', 'Date of Adoption', 'Category Name',
                                'Person Name','Gender' 
                                ]
            table_data_count = len(table_data)
            # we are saving the file on server and storing in table.This id will be used
            # to generate the download link
            date_var = datetime.datetime.now()
            filename    = settings.PROJECT_PATH + '/data_file' + '-' + date_var.isoformat()+'.xlsx'
            writer      = pd.ExcelWriter(filename, engine='xlsxwriter')
            data.to_excel(writer, "sheetname", index=False)
            writer.save()
            dfile = open(filename, 'r')
            obj, created = TrackFile.objects.get_or_create(name_of_file=dfile.name)    
            file_id = obj.id

            # this is the entire data set which got created above and now getting this
            # converted to html for display purpose.
            table_data = table_data.to_html(index=False)


        if state_beneficiary_count_list:
            # this is for beneficiary data, converting to frame 
            beneficiary_data = pd.DataFrame(state_beneficiary_count_list)
            # preparing the data
            beneficiary_data = beneficiary_data[['State', 'Woman of reproductive age (15-49 years)',\
                          'Adolescent girl (10-19 years)', 'Mother of a child 2 to 5 years',\
                          'Mother of a child 6 months to 2 years', 'Mother of a child up to 6 months',\
                          'Pregnant woman']]

            beneficiary_data.columns = ['State', 'Woman of reproductive age (15-49 years)',\
                          'Adolescent girl (10-19 years)', 'Mother of a child 2 to 5 years',\
                          'Mother of a child 6 months to 2 years', 'Mother of a child up to 6 months',\
                          'Pregnant woman']
            # finally converting to html for display purpose.
            beneficiary_data = beneficiary_data.to_html(index=False)
        
        # import pdb;
        # pdb.set_trace()
            ###########################AP Screening Data added in viewrs count############################################
        sum=0;
        if '3' in data_category and len(state) and '6' in state:
            category = [1,2]
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id,\
                                         screening__village__block__district__state_id__in=state).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)
        elif '3' in data_category and len(state)==0:
            category = [1,2]
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)
        

        elif '2' in data_category and len(state) and '6' in state:
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id,\
                                         screening__village__block__district__state_id__in=state).exclude(screening__parentcategory_id=1).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)
        elif '2' in data_category and len(state)==0:
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id).exclude(screening__parentcategory_id=1).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)
        elif '1' in data_category and len(state) and '6' in state:
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id,\
                                         screening__village__block__district__state_id__in=state).filter(screening__parentcategory_id=1).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)
        elif '1' in data_category and len(state)==0:
            total_unique_viewers_AP=AP_Screening.objects.filter(screening__date__range=date_range,\
                                         screening__village__block__district__state__country_id=country.id).filter(screening__parentcategory_id=1).values_list('total_members', flat=True)
            for total in total_unique_viewers_AP:
                sum+=int(total)




        context = {'data_list': table_data, 'beneficiary_data_list': beneficiary_data, 
                   'start_date': date_range[0], 'end_date': date_range[1],
                   'file_id': file_id, 'data_list_count': data_list_count,
                   'table_data_count': table_data_count, 'district_reach': district_reach,
                   'data_category': cd.get('data_category'), 'data': cd.get('data'),
                   'total_screenings': total_screenings, 'total_adoptions' : total_adoptions.get('adoptions'), \
                   'total_viewers': total_unique_viewers.get('unique_viewers')+sum, \
                   'total_unique_adopters': total_adoptions.get('unique_adopters')}
        # import pdb;
        # pdb.set_trace()
        template = "dataexport/table-data.html"
        html = render_to_string(template, context=context)
        return HttpResponse(html)



class DownloadFile(View):

    def get(self, request, *args, **kwargs):
        file_path = TrackFile.objects.get(id=kwargs.get('file_id')).name_of_file
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


class GetState(View):

    def get(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        results = list(State.objects.filter(country_id__in=country_id).values('id','state_name'))
        
        for item in results:
            item['text'] = item.get('state_name')
            item['value'] = int(item.get('id'))
            del item['state_name']
        return JsonResponse({'results': results})







