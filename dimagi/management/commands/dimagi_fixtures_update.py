import urllib2
import os

from django.core.management.base import BaseCommand, CommandError
from poster.streaminghttp import register_openers
from poster.encode import multipart_encode
from dimagi.scripts.create_fixtures_functions import create_fixture
from dimagi.models import CommCareProject, CommCareUser
from dg.settings import MEDIA_ROOT

class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = ''' Deletes fixtures for stated CommCare Project.
    
    Prerequisites:
    (1) Create project in CommCare.
    (2) Enter project information through admin.
    (3) Create atleast one CommCare user for this project.
    (4) Enter user, project and village permissions, through admin.
    '''

    #This file will update fixtures by deleting and reuploading all types of data except Video type from previous database. This done to retain the seasonal behavior   
    def handle(self, *args, **options):
        commcare_project_list = args
        for commcare_project_name in commcare_project_list:
            try:
                commcare_project = CommCareProject.objects.get(name=commcare_project_name)
            except CommCareProject.DoesNotExist:
                raise CommandError('CommCare Project "%s" not yet entered in the Database.' % commcare_project_name)
            commcare_users = CommCareUser.objects.filter(project=commcare_project).all()
        #creates an excel with out seasonal videos
            want_seasonal_behavior = "no"
            create_fixture(commcare_users, commcare_project_name, want_seasonal_behavior)
            
        #deletes old data except videos
            opener = register_openers()
            opener.addheaders =[('User-agent', 'Mozilla/5.0'),
                                     ('user', 'nandinibhardwaj@gmail.com:digitalgreen'),
                                     ('Cookie', 'csrftoken=065b536c11a58f4110e21a163847d1bf; sessionid=71722bedc9fe6efd83e887cb253a79f4; __utma=166502700.894327232.1375426304.1384928721.1385013602.185; __utmb=166502700.17.9.1385013602; __utmc=166502700; __utmz=166502700.1375426304.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)')]
            fixture_url = commcare_project.fixture_url
            response = opener.open(fixture_url)
            
            
            [{"fields": ["id", "low", "high"], "is_global": false, "tag": "video", "name": "Video", "_id": "b24469eb8569a3399c2fb337b632d4e2"}, {"fields": ["id", "name"], "is_global": false, "tag": "unique_video", "name": "Unique_video", "_id": "b24469eb8569a3399c2fb337b6362a19"}, {"fields": ["id", "name", "village_id"], "is_global": false, "tag": "mediator", "name": "Mediator", "_id": "b24469eb8569a3399c2fb337b636cddc"}, {"fields": ["id", "name"], "is_global": false, "tag": "village", "name": "Village", "_id": "b24469eb8569a3399c2fb337b6373f6d"}, {"fields": ["id", "name", "village_id"], "is_global": false, "tag": "group", "name": "Group", "_id": "b24469eb8569a3399c2fb337b63844f7"}]
            
            
            # Data Types Retrieved
            string_response = response.read() 
            types = string_response.split('fields')
            ids_to_delete = {}
            for i in range(len(types)-1):
                ids_to_delete[types[i+1].partition('name": "')[2].partition('",')[0]]=types[i+1].partition('_id": "')[2].partition('"}')[0]
            
            ids_to_delete.pop("Video", None)            
            if len(ids_to_delete) == 0:
                print "Nothing to delete"
            else:
                for name, id in ids_to_delete.items():
                    try:
                        request_string = fixture_url + str(id)
                        request = urllib2.Request(request_string)
                        request.get_method = lambda: 'DELETE'            
                        url = opener.open(request)
                        print "Deleted item : "+str(name)+" with id as "+ str(id)
                    except Exception as ex:
                        print " Could not delete item : " + str (id)
        #uploading new data --- depends on session ID. If this is okay.. Upgrade the code for uploading initial fixtures too - i.e., do fixture upload also like case upload -- avoid uploading manually 
            upload_fixture_url = commcare_project.upload_fixture_url
            filename = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_fixtures_update.xlsx" % (commcare_project_name)) #hardcoded
            params = {'file': open(filename,'rb')}
            datagen, headers = multipart_encode(params)
            request = urllib2.Request(upload_fixture_url, datagen, headers)
            result = urllib2.urlopen(request)
            print "updated fixtures are successfully uploaded"
            