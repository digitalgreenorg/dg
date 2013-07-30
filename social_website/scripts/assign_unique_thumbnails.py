from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from social_website.models import Collection

used_vid_list = []
done = 0
for collection in Collection.objects.all():
    for video in collection.videos.all():
        if video.uid not in used_vid_list:
            collection.thumbnailURL = video.thumbnailURL16by9
            used_vid_list.append(video.uid)
            done += 1
            collection.save()
            break
print '%s collection assigned unique thumbnails' % done
