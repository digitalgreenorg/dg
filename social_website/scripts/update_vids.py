from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from dashboard.models import Video
from social_website.models import Video as Website_video
from social_website.migration_functions import update_website_video

existing_vids = Website_video.objects.all().values_list('coco_id', flat=True)
print len(Video.objects.exclude(id__in = existing_vids))
for video in Video.objects.exclude(id__in = existing_vids):
    update_website_video(video)
    