import json
from social_website.models import Collection, Video, Partner

def enter_data_into_facet_search(conn, index_name):
    i = 0
    for obj in Collection.objects.all():
        vid_data = []
        time = 0
        for index, vid in enumerate(obj.videos.all()):
            vid_id = index+1 
            url = "/social/collections/?id=" + str(obj.uid) + "&video=" + str(vid_id)
            vid_data.append({"title" : vid.title, 
                             "subcategory" : vid.subcategory, 
                             "description" : vid.description,
                             "duration" : vid.duration, 
                             "thumbnailURL" : vid.thumbnailURL16by9, 
                             "youtubeID" : vid.youtubeID,
                             "videoURL" : url})
            time += vid.duration
        
        data = json.dumps({"title" : obj.title,
                           "url" : "", 
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
    # Videos
    for video in Video.objects.all():
        if len(video.collection_set.all()):
            collection = video.collection_set.all()[0]  # choosing the first collection
            for index, vid in enumerate(collection.videos.all()):
                if vid.uid == video.uid:
                    vid_id = index+1 
            url = "/social/collections/?id=" + str(collection.uid) + "&video=" + str(vid_id) 
            data = json.dumps({"searchTerm":video.title, 
                               "targetURL" : url,
                               "type" : "Videos"})
            conn.index(data, index_name, index_name, i+1)
            i+= 1
    
    # Collections        
    for collection in Collection.objects.all():
        if collection.subject != '':
            url = "/social/discover/?title=%s" % str(collection.subject)
            data = json.dumps({"searchTerm" : collection.subject,
                               "targetURL" : url, 
                               "type" : "Collections"}) 
            conn.index(data, index_name, index_name, i+1)
            i+= 1
        if collection.topic != '':
            url = "/social/discover/?title=%s" % str(collection.topic)
            data = json.dumps({"searchTerm" : collection.topic,
                               "targetURL" : url, 
                               "type" : "Collections"}) 
            conn.index(data, index_name, index_name, i+1)
            i+= 1
    
    # Partners
    for partner in Partner.objects.all():
        url = "/social/connect/?id=" + str(partner.uid)
        data = json.dumps({"searchTerm" : partner.name,
                           "targetURL" : url, 
                           "type" : "Partners"}) 
        conn.index(data, index_name, index_name, i+1)
        i+= 1
    print "%s objects of Videos, Collections and Partners added" % i