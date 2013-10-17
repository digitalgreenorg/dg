from django.core.management.base import BaseCommand, CommandError

from dashboard.models import Video
from social_website.models import Video as Website_video
from social_website.migration_functions import update_website_video


class Command(BaseCommand):
    help = '''Run this command when some video from dashboard is not in website tables'''

    def handle(self, *args, **options):
        existing_vids = Website_video.objects.all().values_list('coco_id', flat=True)
        print len(Video.objects.exclude(id__in = existing_vids))
        for video in Video.objects.exclude(id__in = existing_vids):
            update_website_video(video)