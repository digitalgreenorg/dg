import os
import logging
from datetime import timedelta, date, datetime
import json
import urllib2

import isodate
from boto.s3.connection import S3Connection

from videos.models import Video
from dg.settings import ACCESS_KEY, SECRET_KEY, MEDIA_ROOT, GOOGLE_API_KEY
from libs.image_utils import ProcessedImage
from libs.s3_utils import add_to_s3


def get_youtube_entry(youtubeid, url='https://www.googleapis.com/youtube/v3/videos?part=id&id='):
    logger = logging.getLogger('social_website')
    if youtubeid != "":
        try:
            response = urllib2.urlopen(''.join([url, youtubeid, '&key=', GOOGLE_API_KEY]))
            data = json.loads(response.read())
            if int(data['pageInfo']['totalResults']) > 0:
                return data
        except Exception, inst:
            logger.error("YoutubeID: %s Error: %s" % (youtubeid, str(inst)))
    return None


def get_online_stats(yt_entry):
    stats = {
             'views': 0,
             'likes': 0,
            }
    try:
        stats['views'] = int(yt_entry['items'][0]['statistics']['viewCount'])
    except Exception:
        pass
    try:
        stats['likes'] = int(yt_entry['items'][0]['statistics']['likeCount'])
    except Exception:
        pass
    return stats


def cleanup_youtubeid(video_id):
    # Strip spaces at the beginning and end
    video_id = video_id.strip()
    # There shouldn't be any slashes.
    if '/' in video_id:
        # When there is a slash, we have found that the anything before the slash must be removed.
        video_id = video_id.split('/').pop()
    return video_id


def update_video_youtubeid_s3(vid):
    ''' Input: Dashboard Video
    Locates video on YouTube based on youtubeid field
    Creates/updates thumbnails on s3
    Creates/updates duration in duration field
    '''
    # Create S3 Connection
    bucket_name = 'digitalgreen'
    bucket = S3Connection(ACCESS_KEY, SECRET_KEY).create_bucket(bucket_name)
    bucket.set_acl('public-read')
    location_raw_images = 'video_thumbnail/raw/'
    location_16by9_images = 'video_thumbnail/16by9/'

    file_save_dir = os.path.join(MEDIA_ROOT, 'youtube')

    cleaned_id = cleanup_youtubeid(vid.youtubeid)
    if cleaned_id != vid.youtubeid:
        vid.youtubeid = cleaned_id
        vid.save()
    url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2C+contentDetails&id='
    entry = get_youtube_entry(cleaned_id, url)
    if entry:
        # Update thumbnails on s3
        key = "".join([location_raw_images, str(vid.id), '.jpg'])
        if not bucket.get_key(key):
            img = ProcessedImage()
            try:
                url = entry['items'][0]['snippet']['thumbnails']['high']['url']
                filepath = os.path.join(file_save_dir, url.split("/")[-1])
                img.set_image_from_url(url, filepath)
                found_thumbnail = True
            except:
                found_thumbnail = False
            if found_thumbnail:
                img_borderless = img.remove_border()
                filepath_borderless = os.path.join(file_save_dir, ("raw.jpg"))
                img_borderless.save(filepath_borderless)
                add_to_s3(bucket, key, filepath_borderless)
                print key
 
                img_cropped = img_borderless.crop(217, 124)
                filepath_16by9 = os.path.join(file_save_dir, ("16.jpg"))
                img_cropped.save(filepath_16by9)
                key = "".join([location_16by9_images, str(vid.id), '.jpg'])
                add_to_s3(bucket, key, filepath_16by9)
                print key
            else:
                logger = logging.getLogger('social_website')
                logger.info('Image does not exist for youtubeID')
        # Update duration
        duration = isodate.parse_duration(entry['items'][0]['contentDetails']['duration'])
        if vid.duration != str(duration):
            vid.duration = str(duration)
            vid.save()


def call_youtube_update(complete=False):
    vids = Video.objects.exclude(youtubeid='')
    if not complete:
        # Duration is computed using the YouTube API. If this field is not populated, this video record has been newly linked through youtubeid.
        vids = vids.filter(duration=None)

    for video in vids:
        update_video_youtubeid_s3(video)
