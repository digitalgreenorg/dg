from django.core.management.base import BaseCommand, CommandError

from social_website.models import Collection


class Command(BaseCommand):
    help = '''This command will assign the unique thubnails to the collection'''

    def handle(self, *args, **options):
        used_vid_list = []
        done = 0
        for collection in Collection.objects.all():
            vids = collection.videos.all()
            collection.thumbnailURL = vids[0].thumbnailURL16by9
            for video in vids:
                if video.uid not in used_vid_list:
                    collection.thumbnailURL = video.thumbnailURL16by9
                    used_vid_list.append(video.uid)
                    done += 1
                    break
            collection.save()
