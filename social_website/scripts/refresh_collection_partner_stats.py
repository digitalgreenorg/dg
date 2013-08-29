from django.core.management import setup_environ
from django.db.models import Sum
import dg.settings
setup_environ(dg.settings)
from social_website.migration_functions import get_offline_stats, populate_collection_stats, populate_partner_stats
from social_website.models import Collection, Partner, PersonVideoRecord, Video

stats = PersonVideoRecord.objects.all().values('videoID').annotate(views = Sum('views'), likes = Sum('like'), adoptions = Sum('adopted'))
for row in stats:
    try:
        video = Video.objects.get(uid = row['videoID'])
        video.offlineLikes = row['like']
        video.offlineViwes = row['views']
        video.adoptions = row['adoptions']
        video.save()
    except Video.DoesNotExist:
        # Video not yet in website DB
        pass


for collection in Collection.objects.all():
    populate_collection_stats(collection)
    
for partner in Partner.objects.all():
    populate_partner_stats(partner)
    