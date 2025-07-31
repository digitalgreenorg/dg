#coding=utf-8
from dg.settings import *

from django.core.management.base import BaseCommand

from django.db import models

from geographies.models import *
from videos.models import *

from people.models import *

from activities.models import *

import csv, ast, pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        result = []
        person_cat_map = {}
        beneficiary_map = {

                            1: 'Woman of reproductive age (15-49 years)',

                            2: 'Adolescent girl (10-19 years)',

                            3: 'Mother of a child 2 to 5 years',

                            4: 'Mother of a child 6 months to 2 years',

                            5: 'Mother of a child up to 6 months',

                            6: 'Pregnant woman'

                        }
        
        screening_obj_1 = Screening.objects.filter(village__block__district__state_id=3, \
                date__range=['2017-03-01', '2018-09-30'], partner_id=8, \
                videoes_screened__in=[5645, 5646, 5653, 5655, 5656, 5787, 5740, 6142, 6143, 6155, 6156, 6275, 6276, 6277, 6297, 6423, 6481, 6482, 6483, 6484, 6688, 6690, 6691, 6694, 6695, 6696, 6738, 6739, 6963, 6929, 6930, 7027, 5657, 5658, 5910, 6149, 6278, 6479, 6480, 6689, 6692, 6697, 6925, 6698, 7026, 5576, 6311, 6312, 6159, 6313, 6289, 6420, 6485, 6682, 6693, 6971, 6972, 6973])
        
        screening_obj = Screening.objects.filter(village__block__district__state_id=3, \
                date__range=['2017-03-01', '2018-09-30'], partner_id=8, \
                videoes_screened__in=[5645, 5646, 5653, 5655, 5656, 5787, 5740, 6142, 6143, 6155, 6156, 6275, 6276, 6277, 6297, 6423, 6481, 6482, 6483, 6484, 6688, 6690, 6691, 6694, 6695, 6696, 6738, 6739, 6963, 6929, 6930, 7027, 5657, 5658, 5910, 6149, 6278, 6479, 6480, 6689, 6692, 6697, 6925, 6698, 7026, 5576, 6311, 6312, 6159, 6313, 6289, 6420, 6485, 6682, 6693, 6971, 6972, 6973]).\
                values('id', 'date','time_created','user_created_id','user_created__username','videoes_screened')

        video_list = Video.objects.all().values('id','title')
        video_list_frame = pd.DataFrame(list(video_list))
        video_list_frame = video_list_frame.rename(columns={'id':'videoes_screened'})
        video_queryset_frame = pd.DataFrame(list(screening_obj))
        video_queryset_frame = video_queryset_frame.rename(columns={'id':'screening_id'})
        video_screened_merge = pd.merge(video_queryset_frame, video_list_frame, on="videoes_screened")

        queryset = PersonMeetingAttendance.objects.filter(screening_id__in=screening_obj_1)\
                    .values('person_id' ,'screening_id','category')
    
        

        main_queryset_frame = pd.DataFrame(list(queryset))


        screening_merged_with_video_frame = pd.merge(main_queryset_frame, video_screened_merge, on='screening_id')

        #screening_merged_with_video_frame.to_csv('hnn_viewers_odisha.csv')

         
        with open("upvan_1000_days_persons_latest.csv","wb") as f: 
            writer = csv.writer(f)  
            writer.writerow(['Arm-Id','Arm Username','Screening ID','Person ID', 'Screening Field Date', 'Screening System Date',\
                            'Video ID', 'Video Title','Category'])
            
            for index, row in screening_merged_with_video_frame.iterrows():
                category = str(row['category'])
                try:
                    if category is not None and category != "None":
                        cat_ = ast.literal_eval(category)
                        if isinstance(cat_[0], dict):

                                for _dict in cat_:
                                    row_1 = [row['user_created_id'], row['user_created__username'],\
                                            row['screening_id'], row['person_id'], row['date'],\
                                            row['time_created'],\
                                            row['videoes_screened'],row['title'], str(_dict.get('id')) \
                                            ]
                                    writer.writerow(row_1)
                        
                        else:
                            for _id in cat_:
                                row_2 = [row['user_created_id'], row['user_created__username'],\
                                            row['screening_id'], row['person_id'], row['date'],\
                                            row['time_created'],\
                                            row['videoes_screened'],row['title'], str(_id) , \
                                            ]
                                writer.writerow(row_2)
                    else:
                        row_3 = [row['user_created_id'], row['user_created__username'],\
                                    row['screening_id'], row['person_id'], row['date'],\
                                    row['time_created'],\
                                    row['videoes_screened'],row['title'], None  \
                                            ]
                        writer.writerow(row_3)
                        pass
                except Exception as e:
                    print e
                    pass
                
        print '*****************\n*******************\n********************'
        print '*****************\n*******************\n********************'
