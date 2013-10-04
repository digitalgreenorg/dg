import os
import urllib
import logging
from datetime import timedelta, date, datetime
from math import ceil, floor
from PIL import Image

import gdata.youtube.service
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from dg.settings import ACCESS_KEY, SECRET_KEY, MEDIA_ROOT, YOUTUBE_SIMPLE_ACCESS
from dashboard.models import Video


def get_thumbnail(entry, file_save_dir):
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

def cleanup_youtubeid(video_id):
    # Strip spaces at the beginning and end
    video_id = video_id.strip()
    # There shouldn't be any slashes.
    if '/' in video_id:
        # When there is a slash, we have found that the anything before the slash must be removed.
        video_id = video_id.split('/').pop()
    return video_id

def add_to_s3(bucket, key, filepath):
    k = Key(bucket)
    k.key = key
    k.set_contents_from_filename(filepath)
    k.make_public()

def call_youtube_update(complete=False):
    logger = logging.getLogger('dashboard')
    # Create S3 Connection
    bucket_name = 'video_thumbnail'
    bucket = S3Connection(ACCESS_KEY, SECRET_KEY).create_bucket(bucket_name)
    bucket.set_acl('public-read')
    location_raw_images = 'raw/'
    location_16by9_images = '16by9/'

    file_save_dir = os.path.join(MEDIA_ROOT, 'youtube')

    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.developer_key = YOUTUBE_SIMPLE_ACCESS
    # The YouTube API does not currently support HTTPS/SSL access.
    yt_service.ssl = False

    #Check all videos every 7 days. Daily check for new videos only.
    filter_all = (datetime.utcnow().weekday()) % 7 == 0

    vids = Video.objects.exclude(youtubeid='')
    if not (filter_all or complete):
        # Duration is computed using the YouTube API. If this field is not populated, this video record has been newly linked through youtubeid.
        vids = vids.filter(duration=None)

    for vid in vids:
        try:
            cleaned_id = cleanup_youtubeid(vid.youtubeid)
            if cleaned_id == vid.youtubeid:
                vid.youtubeid = cleaned_id
                vid.save()
            #Fetch the video entry from Youtube
            entry = yt_service.GetYouTubeVideoEntry(video_id=cleaned_id)
        except gdata.service.RequestError, inst:
            logger.error("Video ID: %s YoutubeID: %s Error: %s" % (str(vid.id), cleaned_id, str(inst)))
        else:
            # Update thumbnails on s3
            key = "".join([location_raw_images, str(vid.id), '.jpg'])
            if not bucket.get_key(key):
                img = get_thumbnail(entry, file_save_dir)

                img_border = remove_border(img)
                filepath_borderless = os.path.join(file_save_dir, ("raw.jpg"))
                img_border.save(filepath_borderless)
                add_to_s3(bucket, key, filepath_borderless)

                img_cropped = crop(img_border, 217, 124)
                filepath_16by9 = os.path.join(file_save_dir, ("16.jpg"))
                img_cropped.save(filepath_16by9)
                key = "".join([location_16by9_images, str(vid.id), '.jpg'])
                add_to_s3(bucket, key, filepath_16by9)
            # Update duration
            duration = timedelta(seconds = int(entry.media.duration.seconds))
            if vid.duration != str(duration):
                vid.duration = str(duration)
                vid.save()
