from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import gdata.youtube.service
import os
import urllib

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from datetime import timedelta, date, datetime
from math import ceil, floor
from PIL import Image

from dashboard.models import Video

BUCKET_NAME = 'video_thumbnail'
con = S3Connection(dg.settings.ACCESS_KEY, dg.settings.SECRET_KEY)
bucket = con.create_bucket(BUCKET_NAME)
bucket.set_acl('public-read')

file_save_dir = os.path.join(dg.settings.MEDIA_ROOT, 'youtube')


def get_thumbnail(entry):
    for thumbnail in entry.media.thumbnail:
        urllib.urlretrieve(thumbnail.url, os.path.join(file_save_dir, thumbnail.url.split("/")[-1]))
        img = Image.open(os.path.join(file_save_dir, thumbnail.url.split("/")[-1]))
        return img


def remove_border(image):
    sz = image.size
    size = (0, 0, sz[0], sz[1])
    image = image.crop((size[0] + 10, size[1] + 10, size[2] - 10, size[3] - 10))
    img = image.convert('L')
    img1 = img.point(lambda x: 0 if x < 127 else x)
    box = img1.getbbox()
    im_border_removed = image.crop(box)
    return im_border_removed


def crop(img, new_width, new_height):
    ratio = new_width * 1.0 / new_height
    width, height = img.size
    region = {
        'l': 0,
        'r': width,
        'upper': 0,
        'lower': height,
    }
    if width > height * ratio:
        crop = (width - height * ratio) / 2.0
        region['l'] = int(floor(crop))
        region['r'] = int(ceil(width - crop))
    else:
        crop = (height - width / ratio) / 2.0
        region['upper'] = int(floor(crop))
        region['lower'] = int(ceil(height - crop))
    img_crop = img.crop((region['l'], region['upper'], region['r'], region['lower']))
    img_resized = img_crop.resize((new_width, new_height), Image.ANTIALIAS)
    return img_resized


def call_youtube_update(complete=False):
    yt_service = gdata.youtube.service.YouTubeService()

    #Developer key of rahul@digitalgreen.org
    yt_service.developer_key = 'AI39si74a5fwzrBsgSxjgImSsImXHfGgt8IpozLxty9oGP7CH0ky4Hf1eetV10IBi2KlgcgkAX-vmtmG86fdAX2PaG2CQPtkpA'
    # The YouTube API does not currently support HTTPS/SSL access.
    yt_service.ssl = False

    error_ids = {}
    filter_all = (date.today().day) % 7 == 0  #Check all videos every 7 days. Daily check for new videos only.
    if (filter_all or complete):
        vids = Video.objects.exclude(youtubeid='')
    else:
        vids = Video.objects.exclude(youtubeid='').filter(duration=None)

    for vid in vids:
        try:
            #Fetch the video entry from Youtube
            video_id = vid.youtubeid
            video_id = video_id.strip()
            if '/' in video_id:
                video_id_ar = video_id.split('/')
                video_id = video_id_ar[-1]
                vid.youtubeid = video_id
                vid.save()
            entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
        except gdata.service.RequestError, inst:
            error_ids[vid.id] = inst
        else:
            print vid.id
            key = "".join(['raw/', str(vid.id), '.jpg'])
            if not bucket.get_key(key):
                img = get_thumbnail(entry)
                img_border = remove_border(img)
                img_border.save(os.path.join(file_save_dir, ("raw.jpg")))
                k = Key(bucket)
                k.key = key
                k.set_contents_from_filename(os.path.join(file_save_dir, ("raw.jpg")))
                k.make_public()
                img_cropped = crop(img_border, 217, 124)
                img_cropped.save(os.path.join(file_save_dir, ("16.jpg")))
                k = Key(bucket)
                k.key = "".join(['16by9/', str(vid.id), '.jpg'])
                k.set_contents_from_filename(os.path.join(file_save_dir, ("16.jpg")))
                k.make_public()
                print "uploaded to s3"
            duration = timedelta(seconds = int(entry.media.duration.seconds))
            if vid.duration != str(duration):
                vid.duration = str(duration)
                vid.save()

    if(len(error_ids) > 0):
        log = open(dg.settings.MEDIA_ROOT + "log/youtube_log.txt", "a")
        log.write('\n' + str(datetime.utcnow()) + '\n')
        text = ["Following Videos (ID & Error given) have problem with youtube id."]
        for k, v in error_ids.iteritems():
            text.append(str(k) + "\t" + str(v))
        log.write('\n'.join(text))
        log.close()
