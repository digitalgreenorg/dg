from social_website.models import  Collection, Country, Partner, PersonVideoRecord
from social_website.models import Video
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.loading import get_model
from django.db.models import Count, Sum
import gdata.youtube.service

S3_VIDEO_BUCKET = r'http://s3.amazonaws.com/video_thumbnail/raw/'
DEVELOPER_KEY = 'AI39si74a5fwzrBsgSxjgImSsImXHfGgt8IpozLxty9oGP7CH0ky4Hf1eetV10IBi2KlgcgkAX-vmtmG86fdAX2PaG2CQPtkpA'

def add_partner_info(partner):
    website_partner = Partner(uid=str(partner.id), joinDate=partner.date_of_association, name=partner.partner_name,
                              logoURL = '', description = '', # add after description and logo in dashboard have been made
                              collectionCount = 0, videos = 0, views = 0,likes = 0, adoptions = 0) # since default=0 is not given
    website_partner.save()

def get_offline_stats(video_id):
    stats = PersonVideoRecord.objects.filter(videoID = video_id).aggregate(Sum('like'), Sum('views'), Sum('adopted'))
    return stats

def update_person_video_record(pma):
    from dashboard.models import PersonMeetingAttendance
    person_video_list = PersonMeetingAttendance.objects.filter(id = pma.id).values_list('person', 'screening__videoes_screened','interested')
    for person, video, interested in person_video_list:
        try:
            person_video_obj = PersonVideoRecord.objects.get(personID = person, videoID= video)
            person_video_obj.views += 1
            if interested:
                person_video_obj.like = 1
        except ObjectDoesNotExist:
            person_video_obj = PersonVideoRecord(personID = person, videoID = video, like = interested, views = 1)
        person_video_obj.save()
  
def check_video_youtube_id(vid):
    if vid.youtubeid != "" :
        try:
            yt_service = gdata.youtube.service.YouTubeService()
            yt_service.developer_key = DEVELOPER_KEY
            yt_service.ssl = False
            entry = yt_service.GetYouTubeVideoEntry(video_id = vid.youtubeid)
            if entry is not None:
                return entry
        except Exception, ex:
            pass
    return None
    
def get_online_stats(yt_entry):     
    stats = {}
    stats['views'] = int(yt_entry.statistics.view_count) 
    stats['duration'] = int(yt_entry.media.duration.seconds)
    if yt_entry.rating:
        stats['likes'] = int((float(yt_entry.rating.average)*float(yt_entry.rating.num_raters)-float(yt_entry.rating.num_raters))/4)
    else:
        stats['likes'] = 0         
    return stats
      
def update_website_video(vid):
    from dashboard.models import Partners, Language
    yt_entry = check_video_youtube_id(vid)
    if yt_entry: 
        partner = Partner.objects.get(uid = str(vid.village.block.district.partner.id))
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
        website_vid = Video(uid = str(vid.id), title = vid.title, description = vid.summary, youtubeID = vid.youtubeid, date = vid.video_production_end_date,
                            sector = sector, subsector = subsector, topic = topic, subtopic = subtopic, subject = subject,
                            thumbnailURL = thumbnailURL, thumbnailURL16by9 = '',thumbnailURL4by3 = '',
                            language = language, partner = partner, state = state,
                            offlineLikes = offline_stats['like__sum'], offlineViews = offline_stats['views__sum'], adoptions = offline_stats['adopted__sum'], 
                            onlineLikes = online_stats['likes'], duration = online_stats['duration'], onlineViews = online_stats['views'],
                            )
        website_vid.save()
        
def get_collection_pracs(videos,field1,field2,field3,field4):
    pracs = {}
    pracs[field1] = videos[0].sector if len(set(videos.values_list(field1)))==1 else ''
    pracs[field2] = videos[0].subsector if len(set(videos.values_list(field2)))==1 else ''
    pracs[field3] = videos[0].subtopic if len(set(videos.values_list(field3)))==1 else ''
    pracs[field4] = videos[0].subject if len(set(videos.values_list(field4)))==1 else ''
    return pracs
    
def populate_country(country):
        website_country = Country(countryName = country.country_name)
        website_country.save()
        
def create_collections():
    from dashboard.models import Partners
    collection_counter = 1 #remove when collection id is Autofield
    
    ####### COLLECTIONS BASED ON TOPIC ##############################
    collection_combinations = Video.objects.exclude(topic = '').values_list('partner_id','language','topic','state').annotate(vids = Count('uid')).filter(vids__gte=5, vids__lte=25)
    for partner, language, topic, state, count in collection_combinations:
        videos = Video.objects.filter(partner_id = partner, language = language ,topic = topic, state = state)
        collection_pracs = get_collection_pracs(videos,'sector','subsector','subtopic','subject')
        country = Country.objects.get(countryName = Partners.objects.get(id = partner).district_set.all()[0].state.country.country_name) 
        website_collection = Collection(uid = str(collection_counter), #remove when uid is AutoField
                                        state = state, country = country, partner = Partner.objects.get(uid=partner), language = language,
                                        category = collection_pracs['sector'], subcategory = collection_pracs['subsector'], topic = topic, 
                                        subtopic = collection_pracs['subtopic'],  subject = collection_pracs['subject'],
                                        title = videos[0].topic, thumbnailURL = '') # update thumbnail with Aadish's migration
        website_collection.save()
        for video in videos:
            website_collection.videos.add(video)
        collection_counter += 1
    
    ####### COLLECTIONS BASED ON SUBJECT #############################    
    collection_combinations = Video.objects.exclude(subject = '').values_list('partner_id','language','subject','state').annotate(vids = Count('uid')).filter(vids__gte=5, vids__lte=25)
    for partner, language, subject, state, count in collection_combinations:
        videos = Video.objects.filter(partner_id = partner, language = language, subject = subject, state = state)
        collection_pracs = get_collection_pracs(videos,'sector','subsector','topic','subtopic',)
        country = Country.objects.get(countryName = Partners.objects.get(id = partner).district_set.all()[0].state.country.country_name) 
        website_collection = Collection(uid = str(collection_counter), #remove when uid is AutoField
                                        state = state, country = country, partner = Partner.objects.get(uid=partner), language = language,
                                        category = collection_pracs['sector'], subcategory = collection_pracs['subsector'], topic = collection_pracs['topic'], 
                                        subtopic = collection_pracs['subtopic'],  subject = subject,
                                        title = videos[0].subject, thumbnailURL = '') # update thumbnail with Aadish's migration
        website_collection.save()
        for video in videos:
            website_collection.videos.add(video)
        collection_counter += 1
        