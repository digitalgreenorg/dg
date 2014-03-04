from django.core.urlresolvers import reverse
import json
from social_website.models import Collection, Video, Partner

def get_absolute_url_for_completion(self):
    return reverse('social_website.views.search_view')

def enter_data_into_facet_search(conn, index_name):
    i = 0
    for obj in Collection.objects.all():
        vid_data = []
        time = 0
        for index, vid in enumerate(obj.videos.all()):
            vid_id = index+1 
            url = obj.get_absolute_url_for_video(vid_id)
            vid_data.append({"title" : vid.title, 
                             "subcategory" : vid.subcategory, 
                             "description" : vid.description,
                             "duration" : vid.duration, 
                             "thumbnailURL" : vid.thumbnailURL16by9, 
                             "youtubeID" : vid.youtubeID,
                             "videoURL" : url})
            time += vid.duration
        
        data = json.dumps({"title" : obj.title,
                           "url" : obj.get_absolute_url(), 
                           "language" : obj.language,
                           "partner" : obj.partner.name,
                           "state" : obj.state,
                           "category" : obj.category,
                           "subcategory" : obj.subcategory, 
                           "topic": obj.topic, 
                           "subject" : obj.subject, 
                           "likes" : obj.likes, 
                           "views" : obj.views, 
                           "adoptions" : obj.adoptions,
                           "thumbnailURL" : obj.thumbnailURL,
                           "uid" : obj.uid,
                           "videos" : vid_data,
                           "duration" : time
                           })    
        conn.index(data, index_name, index_name,i+1)
        i+= 1
    print "%s Collections added into facet search" % i

def enter_data_into_completion_search(conn, index_name):
    i = 0
    non_collection = 0
    # Videos
    for video in Video.objects.all():
        if len(video.collection_set.all()):
            collection = video.collection_set.all()[0]  # choosing the first collection
            for index, vid in enumerate(collection.videos.all()):
                if vid.uid == video.uid:
                    vid_id = index+1 
            url = collection.get_absolute_url_for_video(vid_id)
            data = json.dumps({"searchTerm":video.title, 
                               "targetURL" : url,
                               "type" : "Videos"})
            conn.index(data, index_name, index_name, i+1)
            i+= 1
        else:
            url = video.get_absolute_url()
            data = json.dumps({"searchTerm":video.title, 
                               "targetURL" : url,
                               "type" : "Videos"})
            conn.index(data, index_name, index_name, i+1)
            i+= 1
            non_collection += 1
    print "%d videos without collections added" % non_collection
    
    # Collections        
    for collection in Collection.objects.all():
        if collection.subject != '':
            url = '%s/?title=%s' % (get_absolute_url_for_completion(collection), collection.subject)
            data = json.dumps({"searchTerm" : collection.subject,
                               "targetURL" : url, 
                               "type" : "Collections"}) 
            conn.index(data, index_name, index_name, i+1)
            i+= 1
        if collection.topic != '':
            url = '%s/?title=%s' % (get_absolute_url_for_completion(collection), collection.topic)
            data = json.dumps({"searchTerm" : collection.topic,
                               "targetURL" : url, 
                               "type" : "Collections"}) 
            conn.index(data, index_name, index_name, i+1)
            i+= 1
    
    # Partners
    for partner in Partner.objects.all():
        url = partner.get_absolute_url()
        data = json.dumps({"searchTerm" : partner.name,
                           "targetURL" : url, 
                           "type" : "Partners"}) 
        conn.index(data, index_name, index_name, i+1)
        i+= 1
    print "%s objects of Videos, Collections and Partners added" % i

def enter_data_into_video_search(conn, index_name):
    i = 0
    for obj in Video.objects.all():
        if len(obj.collection_set.all()):
            collection = obj.collection_set.all()[0]  # choosing the first collection
            for index, vid in enumerate(collection.videos.all()):
                if vid.uid == obj.uid:
                    vid_id = index+1 
            url = collection.get_absolute_url_for_video(vid_id)
        else:
            url = obj.get_absolute_url()
        data = json.dumps({"title" : obj.title,
                           "url" : url, 
                           "language" : obj.language,
                           "partner" : obj.partner.name,
                           "state" : obj.state,
                           "category" : obj.category,
                           "subcategory" : obj.subcategory, 
                           "topic": obj.topic, 
                           "subject" : obj.subject, 
                           "thumbnailURL" : obj.thumbnailURL16by9,
                           "uid" : obj.uid,
                           "duration" : obj.duration,
                           "description" : obj.description
                           })    
        conn.index(data, index_name, index_name,i+1)
        i+= 1
    print "%s Videos added into video search" % i