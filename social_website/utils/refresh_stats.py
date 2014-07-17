from django.core.management import setup_environ
from django.db.models import Sum

from social_website.migration_functions import get_online_stats, populate_collection_stats, populate_partner_stats
from social_website.models import Collection, Partner, PersonVideoRecord, Video, VideoLike
from libs.youtube_utils import get_youtube_entry


def refresh_collection_partner_stats():
    for collection in Collection.objects.all():
        populate_collection_stats(collection)

    for partner in Partner.objects.all():
        populate_partner_stats(partner)

def refresh_offline_stats():
    stats = PersonVideoRecord.objects.all().values('videoID').annotate(views = Sum('views'), likes = Sum('like'), adoptions = Sum('adopted'))
    for row in stats:
        try:
            video = Video.objects.get(coco_id = row['videoID'])
            video.offlineLikes = row['likes']
            video.offlineViews = row['views']
            video.adoptions = row['adoptions']
            video.save()
        except Video.DoesNotExist:
            # Video not yet in website DB
            pass

def refresh_online_stats():
    for vid in Video.objects.all():
        yt_entry = get_youtube_entry(vid.youtubeID)
        if yt_entry:
            online_stats = get_online_stats(yt_entry)
            vid.onlineViews = online_stats['views']
            vid.onlineLikes = int(online_stats['likes']) + VideoLike.objects.filter(video=vid.uid).count()
            vid.save()
