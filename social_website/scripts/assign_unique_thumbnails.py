from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from social_website.models import Collection

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
print '%s collection assigned unique thumbnails' % done
