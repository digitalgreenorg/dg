import gc
from collections import defaultdict 

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum

import gdata.youtube.service
from libs.youtube_utils import cleanup_youtubeid, get_youtube_entry, get_online_stats
from social_website.models import Collection, Comment, Partner, Person, PersonVideoRecord, Video


S3_VIDEO_BUCKET = r'http://s3.amazonaws.com/video_thumbnail/raw/'
DEVELOPER_KEY = 'AI39si74a5fwzrBsgSxjgImSsImXHfGgt8IpozLxty9oGP7CH0ky4Hf1eetV10IBi2KlgcgkAX-vmtmG86fdAX2PaG2CQPtkpA'
S3_FARMERBOOK_URL = "https://s3.amazonaws.com/dg_farmerbook/2/"

def initial_personvideorecord():
    from dashboard.models import PersonAdoptPractice, PersonMeetingAttendance
    person_video_adoption_dict = defaultdict(dict)
    paps = PersonAdoptPractice.objects.all().values('person_id', 'video_id')
    for pap_row in paps:
        if pap_row['video_id'] in person_video_adoption_dict[pap_row['person_id']]:
            person_video_adoption_dict[pap_row['person_id']][pap_row['video_id']] += 1
        else:
            person_video_adoption_dict[pap_row['person_id']][pap_row['video_id']] = 1
    del paps
    
    person_screening_dict = defaultdict(list)        
    pmas = PersonMeetingAttendance.objects.all().values('person_id', 'screening__videoes_screened', 'interested')
    for pma_row in pmas:
        if pma_row['screening__videoes_screened']:
            person_screening_dict[pma_row['person_id']].append({'vid' : pma_row['screening__videoes_screened'], 'interested' : pma_row['interested']})
    del pmas
    gc.collect()
    record_list = []
    chunk = 20000
    i = 0
    for person_id, videos_info in person_screening_dict.iteritems():
        vid_dict = defaultdict(dict)
        for row in videos_info:
            if row['vid'] in vid_dict:
                vid_dict[row['vid']]['views'] += 1
                if row['interested']:
                    vid_dict[row['vid']]['interested'] = 1
            else:
                vid_dict[row['vid']]['views'] = 1
                vid_dict[row['vid']]['interested'] = 1 if row['interested'] else 0
            
        for vid_id, vals in vid_dict.iteritems():
            adopted = person_video_adoption_dict[person_id][vid_id] if vid_id in person_video_adoption_dict[person_id] else 0 
            record_list.append(PersonVideoRecord(personID = person_id, videoID = vid_id, views = vals['views'], like =  vals['interested'], adopted = adopted))
            i += 1
            if i%chunk == 0:
                PersonVideoRecord.objects.bulk_create(record_list)
                print "%s" % (i)
                del record_list
                record_list = []
    if record_list:
        PersonVideoRecord.objects.bulk_create(record_list)
        
def add_partner_info(partner):
    website_partner = Partner(coco_id = str(partner.id), joinDate = partner.date_of_association, name = partner.partner_name,
                              logoURL = '', description = '', full_name = ' ')
    website_partner.save()

def get_offline_stats(video_id):
    stats = PersonVideoRecord.objects.filter(videoID = video_id).aggregate(Sum('like'), Sum('views'), Sum('adopted'))
    stats['like__sum'] = stats['like__sum'] if stats['like__sum'] is not None else 0
    stats['views__sum'] = stats['views__sum'] if stats['views__sum'] is not None else 0
    stats['adopted__sum'] = stats['adopted__sum'] if stats['adopted__sum'] is not None else 0 
    return stats

def update_person_video_record(pma, videos):
    for video in videos:
        try:
            person_video_obj = PersonVideoRecord.objects.get(personID = pma.person_id, videoID = video.id)
            person_video_obj.views += 1
            if pma.interested:
                person_video_obj.like = 1
        except ObjectDoesNotExist:
            person_video_obj = PersonVideoRecord(personID = pma.person_id, videoID = video.id, like = pma.interested, views = 1)
        person_video_obj.save()

def populate_adoptions(pap):
    person_id = pap.person_id
    video_id = pap.video_id
    try:
        person_vid_obj = PersonVideoRecord.objects.get(personID = person_id, videoID = video_id)
        person_vid_obj.adopted += 1
        person_vid_obj.save()
    except ObjectDoesNotExist:
        pass
      
def update_website_video(vid):
    yt_entry = get_youtube_entry(cleanup_youtubeid(vid.youtubeid))
    if yt_entry: 
        partner = Partner.objects.get(coco_id = str(vid.village.block.district.partner.id))
        language  = vid.language.language_name
        state = vid.village.block.district.state.state_name
        date = vid.video_production_end_date
        offline_stats = get_offline_stats(vid.id)
        online_stats = get_online_stats(yt_entry)
        if vid.related_practice is not None:
            sector = vid.related_practice.practice_sector.name if vid.related_practice.practice_sector else ''
            subsector = vid.related_practice.practice_subsector.name if vid.related_practice.practice_subsector else ''
            topic = vid.related_practice.practice_topic.name if vid.related_practice.practice_topic else ''
            subtopic = vid.related_practice.practice_subtopic.name if vid.related_practice.practice_subtopic else ''
            subject = vid.related_practice.practice_subject.name if vid.related_practice.practice_subject else ''
        else:
            sector = subsector = topic = subtopic = subject = ''
        thumbnailURL = S3_VIDEO_BUCKET + str(vid.id) + '.jpg'
        try :
            website_vid = Video.objects.get(coco_id = str(vid.id))
            # There is just one result for a filter, but we want to use update here.
            website_vid = Video.objects.filter(coco_id = str(vid.id))
            website_vid.update(title = vid.title, description = vid.summary, youtubeID = vid.youtubeid, date = vid.video_production_end_date,
                                category = sector, subcategory = subsector, topic = topic, subtopic = subtopic, subject = subject,
                                language = language, partner = partner, state = state,
                                offlineLikes = offline_stats['like__sum'], offlineViews = offline_stats['views__sum'], adoptions = offline_stats['adopted__sum'], 
                                onlineLikes = online_stats['likes'], duration = online_stats['duration'], onlineViews = online_stats['views'],
                                thumbnailURL = "http://s3.amazonaws.com/video_thumbnail/raw/%s.jpg" % str(vid.id),
                                thumbnailURL16by9 = "http://s3.amazonaws.com/video_thumbnail/16by9/%s.jpg" % str(vid.id))
        except Video.DoesNotExist:
            website_vid = Video(coco_id = str(vid.id), title = vid.title, description = vid.summary, youtubeID = vid.youtubeid, date = vid.video_production_end_date,
                                category = sector, subcategory = subsector, topic = topic, subtopic = subtopic, subject = subject,
                                language = language, partner = partner, state = state,
                                offlineLikes = offline_stats['like__sum'], offlineViews = offline_stats['views__sum'], adoptions = offline_stats['adopted__sum'], 
                                onlineLikes = online_stats['likes'], duration = online_stats['duration'], onlineViews = online_stats['views'],
                                thumbnailURL = "http://s3.amazonaws.com/video_thumbnail/raw/%s.jpg" % str(vid.id),
                                thumbnailURL16by9 = "http://s3.amazonaws.com/video_thumbnail/16by9/%s.jpg" % str(vid.id))
            website_vid.save()
        
def get_collection_pracs(videos,field1,field2,field3,field4,field5):
    pracs = {}
    pracs[field1] = videos[0].category if len(set(videos.values_list(field1)))==1 else ''
    pracs[field2] = videos[0].subcategory if len(set(videos.values_list(field2)))==1 else ''
    pracs[field3] = videos[0].topic if len(set(videos.values_list(field3)))==1 else ''
    pracs[field4] = videos[0].subtopic if len(set(videos.values_list(field4)))==1 else ''
    pracs[field5] = videos[0].subject if len(set(videos.values_list(field5)))==1 else ''
    return pracs
        
def create_collections():
    ####### COLLECTIONS BASED ON TOPIC ##############################
    collection_combinations = Video.objects.exclude(topic = '').values_list('partner_id','language','topic','state').annotate(vids = Count('uid')).filter(vids__gte=5, vids__lte=25)
    for partner, language, topic, state, count in collection_combinations:
        videos = Video.objects.filter(partner_id = partner, language = language ,topic = topic, state = state)
        collection_pracs = get_collection_pracs(videos,'category','subcategory','topic','subtopic','subject')
        website_collection = Collection(state = state, partner = Partner.objects.get(uid=partner), language = language,
                                        category = collection_pracs['category'], subcategory = collection_pracs['subcategory'], topic = topic, 
                                        subtopic = collection_pracs['subtopic'],  subject = collection_pracs['subject'],
                                        title = videos[0].topic, thumbnailURL = '') # update thumbnail with Aadish's migration
        website_collection.save()
        for video in videos:
            website_collection.videos.add(video)
    
    ####### COLLECTIONS BASED ON SUBJECT #############################    
    collection_combinations = Video.objects.exclude(subject = '').values_list('partner_id','language','subject','state').annotate(vids = Count('uid')).filter(vids__gte=5, vids__lte=25)
    for partner, language, subject, state, count in collection_combinations:
        videos = Video.objects.filter(partner_id = partner, language = language, subject = subject, state = state)
        collection_pracs = get_collection_pracs(videos,'category','subcategory','topic','subtopic','subject')
        website_collection = Collection(state = state, partner = Partner.objects.get(uid=partner), language = language,
                                        category = collection_pracs['category'], subcategory = collection_pracs['subcategory'], topic = collection_pracs['topic'], 
                                        subtopic = collection_pracs['subtopic'],  subject = subject,
                                        title = videos[0].subject, thumbnailURL = '') # update thumbnail with Aadish's migration
        website_collection.save()
        for video in videos:
            website_collection.videos.add(video)
        
def populate_collection_stats(collection):
    stats = collection.videos.all().aggregate(Sum('offlineLikes'), Sum('offlineViews'), Sum('adoptions'), Sum('onlineLikes'), Sum('onlineViews'))
    collection.likes = stats['offlineLikes__sum'] + stats['onlineLikes__sum']
    collection.views = stats['offlineViews__sum'] + stats['onlineViews__sum']
    collection.adoptions = stats['adoptions__sum']
    collection.save()    
    
def populate_partner_stats(partner):
    stats = Video.objects.filter(partner_id = partner.uid).aggregate(Count('uid'), Sum('onlineLikes'), Sum('offlineLikes'), Sum('onlineViews'), Sum('offlineViews'), Sum('adoptions'))
    if stats['uid__count'] > 0:                 #check if partner has at least one video
        partner.video_count = stats['uid__count']
        partner.likes = stats['onlineLikes__sum'] + stats['offlineLikes__sum']
        partner.views = stats['onlineViews__sum'] + stats['offlineViews__sum']
        partner.adoptions = stats['adoptions__sum']
    partner.collection_count = Collection.objects.filter(partner = partner).count()
    partner.save()
        
def populate_farmers(person):
    partner = Partner.objects.get(coco_id = str(person.village.block.district.partner.id))
    try:
        website_farmer = Person.objects.get(coco_id = str(person.id))
        # There is just one result for a filter, but we want to use update here.
        website_farmer = Person.objects.filter(coco_id = str(person.id))
        website_farmer.update(coco_id = str(person.id), name = person.person_name, 
                                                                                partner = partner,thumbnailURL = S3_FARMERBOOK_URL + str(person.id) + '.jpg')
    except Person.DoesNotExist:
        website_farmer = Person(coco_id = str(person.id), name = person.person_name, partner = partner,
                                thumbnailURL = S3_FARMERBOOK_URL + str(person.id) + '.jpg')
        website_farmer.save()

def update_questions_asked(pma):
    if pma.expressed_question != '':
        videos = [video for video in pma.screening.videoes_screened.all()]
        for dashboard_video in videos:
            try:
                video = Video.objects.get(coco_id = str(dashboard_video.id))
                if Comment.objects.filter(video = video, text = pma.expressed_question):
                    return 
                person = Person.objects.get(coco_id = str(pma.person_id))
                comment = Comment(date = pma.screening.date, text = pma.expressed_question, isOnline=False, person = person, video = video) 
                comment.save()
            except Exception as ex:
                # this means either person or video does not exist on website DB
                pass
            
def delete_person(person):
    website_person = Person.objects.get(coco_id = str(person.id))
    comments = Comment.objects.filter(person = website_person)
    comments.delete()
    website_person.delete()
    
def delete_video(video):
    website_video = Video.objects.get(coco_id = str(video.id))
    comments = Comment.objects.filter(video = website_video)
    comments.delete()
    website_video.delete()
