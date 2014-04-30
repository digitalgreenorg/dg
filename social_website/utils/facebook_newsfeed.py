import json
import logging
import urllib
import urllib2

from dg.settings import MEDIA_ROOT, MEDIA_URL, PROJECT_PATH, STATIC_URL
from dg.settings import SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET
from libs.image_utils import ProcessedImage
from social_website.utils.generate_activities import ActivityType
from social_website.models import Activity, ImageSpec


def create_thumbnail(url, image_name, new_width, new_height):
    image = ProcessedImage()
    filepath = MEDIA_ROOT + 'facebook/' + image_name
    image.set_image_from_url(url, filepath)
    cropped_image = image.crop(new_width, new_height)
    cropped_image.save(filepath)
    return ''.join([MEDIA_URL, "facebook/", image_name])

def read_data(entry):
    '''
    Returns True if the entry is already in the database, therefore the feed has been completely processed.
    Returns False otherwise
    '''
    has_image = False
    facebookID = entry['id'].split('_')[-1]
    image_url = ""
    altString = ""
    imageLinkURL = ""
    
    # Do not add the activity if another activity with the same Facebook ID has already been added.
    
    if Activity.objects.filter(facebookID=facebookID).count() > 0:
        return True
    # We look at entry 'types' photo, link and video. And no others.
    # An entry of type 'photo' is found to contain 'message', 'caption' or 'story'. These fields contain text typed by the Facebook user. We discard those those which don't have atleast one of these.
    if entry['type'] == 'photo':
        title = entry['name'] if 'name' in entry else "Digital Green"
        if 'message' in entry:
            textContent = entry['message']
        elif 'caption' in entry:
            textContent = entry['caption']
        elif 'story' in entry:
            textContent = entry['story']
        else:
            # Ignore this entry
            return False
        if 'picture' in entry:
            try:
                # Facebook returns image 
                picture = entry['picture'].replace("_s", "_n")
                # TODO: what if there is more than one _s??
                # Can we upload to s3 here
                image_name = ''.join([facebookID, ".", picture.split('.')[-1]])
                image_url = create_thumbnail(picture, image_name, 170, 112)
                altString = "Image from Facebook"
                imageLinkURL = entry['link'] if 'link' in entry else ''
                has_image = True
            except:
                # Images are not there or url was not accessed.
                # Ignore the picture and continue
                # TODO: How do we find bugs here?
                pass
    # An entry of type 'link' or 'video' is found to contain 'message' or 'description'. These fields contain text typed by the Facebook user. We discard those those which don't have atleast one of these. 
    elif (entry['type'] == 'link' or entry['type'] == 'video'):
        title = entry['name'] if 'name' in entry else 'Digital Green Shared ' + entry['type'].title()
        if 'message' in entry:
            textContent = entry['message']
        elif 'description' in entry:
            textContent = entry['description']
        else:
            # If there is message or description, ignore this entry
            return False
        if 'picture' in entry:
            try:
                picture = urllib2.unquote(entry['picture']).split('url=')[-1]
                image_name = ''.join([facebookID, ".", (picture.split('.')[-1])[:3]])
                image_url = create_thumbnail(picture, image_name, 170, 112)
                altString = "Image from Facebook"
                imageLinkURL = entry['link'] if 'link' in entry else ''
                has_image = True
            except:
                pass
    else:
        return False
    date = entry['created_time'].split('T')[0]
    avatarURL = ''.join([STATIC_URL, 'assets/images/favicon-white.png'])
    newsFeed = 1
    activity_type = ActivityType.facebook
    titleURL = 'https://www.facebook.com/digitalgreenorg/posts/' + facebookID
    store_data(title, date, textContent, avatarURL, newsFeed, image_url, altString, imageLinkURL, facebookID, has_image, activity_type, titleURL)
    return False

def store_data(title, date, textContent, avatarURL, newsFeed, imageURL, altString, imageLinkURL, facebookID, has_image, activity_type, titleURL):
    activity = None
    if title not in ["Digital Green", "Timeline Photos"] and Activity.objects.filter(title=title, type=activity_type).count() > 0:
        activity = Activity.objects.get(title=title, type=activity_type)
        # TODO: What if MultipleObjectsReturned?
    else:
        activity = Activity(title=title, date=date, textContent=textContent, avatarURL=avatarURL, newsFeed=newsFeed, facebookID=facebookID, type=activity_type, titleURL=titleURL)
        activity.save()
    if has_image and activity is not None:
        image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
        image_spec_entry.save()
        activity.images.add(image_spec_entry)
        activity.save()


def get_facebook_feed():
    logger = logging.getLogger('social_website')
    TOKEN_URL = "".join(['https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=', SOCIAL_AUTH_FACEBOOK_KEY, '&client_secret=', SOCIAL_AUTH_FACEBOOK_SECRET])
    response = urllib2.urlopen(TOKEN_URL)
    TOKEN = response.read()
    RESPONSE_URL = 'https://graph.facebook.com/digitalgreenorg/feed?' + TOKEN

    get_more_entries = True
    entries = []
    while(get_more_entries):
        if not entries:
            response = urllib2.urlopen(RESPONSE_URL)
            data = json.loads((response.read()))
            if 'paging' in data:
                RESPONSE_URL = data['paging']['next']
                entries = data['data']
                entries.reverse()
            else:
                get_more_entries = False
        else:
            repeated = read_data(entries.pop())
            if repeated:
                get_more_entries = False
    logger.info("Newsfeed Updated")
