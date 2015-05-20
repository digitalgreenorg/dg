import os
from os import listdir
from boto.s3.connection import S3Connection

import csv

from django.core.management.base import BaseCommand

from libs.s3_utils import add_to_s3
from dg.settings import ACCESS_KEY, SECRET_KEY, MEDIA_ROOT, YOUTUBE_SIMPLE_ACCESS
from videos.models import Video
from social_website.models import Video as website_video
from videokheti.models import ActionType, Crop, Method, TimeYear, Video as videokheti_video


class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = '''Creates initial cases for a new CommCare Application. Prerequisites:
    (1) Create project in CommCare.
    (2) Enter project information through admin.
    (3) Create atleast one CommCare user for this project.
    (4) Enter user, project and village permissions, through admin.
    '''

    def handle(self, *args, **options):
        bucket_name = 'videokheti_audio'
        bucket = S3Connection(ACCESS_KEY, SECRET_KEY).create_bucket(bucket_name)
        bucket.set_acl('public-read')
        #__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        #csvfile = open(os.path.join(__location__, 'mediator_transfer.csv'), 'rb')
        #reader = csv.DictReader(csvfile)
        #onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
        # Adding Videos Name to S3 #
        #=======================================================================
        # for f in listdir('C:/Users/Aadish/Desktop/audio'):
        #     print f
        #     video_id = f.split('.')[0]
        #     print video_id
        #     video_obj = Video.objects.get(old_coco_id=video_id)
        #     print video_obj.title
        #     key = ''.join([str(video_obj.id), '.mp3'])
        #     filepath = ''.join(['C:/Users/Aadish/Desktop/audio\\', f])
        #     if not bucket.get_key(key):
        #         add_to_s3(bucket, key, filepath)
        #=======================================================================

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        csvfile = open(os.path.join(__location__, 'video.csv'), 'rb')
 
        dict_video = {}
        reader = csv.DictReader(csvfile)
        for i in reader:
            if i['VideoID'] not in dict_video:
                dict_video[i['VideoID']] = (i['Crop'], i['TimeYear'], i['ActionType'],i['Method'])
        #print dict_video
 
        rs = bucket.list()
 
        for key in rs:
            video_id = key.name.split('.')[0]
            coco_video = Video.objects.get(id=video_id)
            try:
                webs_video = website_video.objects.get(coco_id=video_id)
                #print dict_video[str(coco_video.old_coco_id)]
                read_tuple = dict_video[str(coco_video.old_coco_id)]
                crop = Crop.objects.get(name=read_tuple[0])
                time_year = TimeYear.objects.get(name=read_tuple[1])
                action_type = ActionType.objects.get(name=read_tuple[2]) if read_tuple[2] != '-' else None
                method = Method.objects.get(name=read_tuple[3]) if read_tuple[3] != '-' else None
                image_file = ''.join(['https://s3.amazonaws.com/digitalgreen/video_thumbnail/16by9/', str(coco_video.id), '.jpg'])
                sound_file = ''.join(['https://s3.amazonaws.com/videokheti_audio/', str(coco_video.id), '.mp3'])
                kheti_video = videokheti_video(coco_video=coco_video, website_id=str(webs_video.uid), 
                                               crop = crop, time_year=time_year, action_type=action_type,
                                               method = method,
                                               image_file=image_file,
                                               sound_file=sound_file,
                                               )
                kheti_video.save()
            except Exception as inst:
                print video_id
                print inst
  
