from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from social_website.migration_functions import get_offline_stats, populate_collection_stats, populate_partner_stats
from social_website.models import Collection, Partner, Video

for video in Video.objects.all():
    stats = get_offline_stats(video.coco_id)
    video.offlineLikes = stats['like__sum']
    video.offlineViews = stats['views__sum']
    video.adoptions = stats['adopted__sum']
    video.save()

for collection in Collection.objects.all():
    populate_collection_stats(collection)
    
for partner in Partner.objects.all():
    populate_partner_stats(partner)
    