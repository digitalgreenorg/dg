import urllib
import urllib2
import json

from dg.settings import APP_ID_FACEBOOK, APP_SECRET_FACEBOOK, PROJECT_PATH
from math import floor, ceil
from PIL import Image
from social_website.models import Activity, ImageSpec


def crop_thumbnail(img, ratio, filename):
    width, height = img.size
    left = 0
    upper = 0
    right = width
    lower = height
    if (width > height):
        new_width = (float)(ratio[0] * height) / ratio[1]
        if (new_width < width):
            left = (width - new_width) / 2.0
            right = right - (width - new_width) / 2.0
        else:
            new_height = (float)(ratio[1] * width) / ratio[0]
            upper = (height - new_height) / 2.0
            lower = lower - (height - new_height) / 2.0
    else:
        new_height = (float)(ratio[1] * width) / ratio[0]
        if (new_height < height):
            upper = (height - new_height) / 2.0
            lower = lower - (height - new_height) / 2.0
        else:
            new_width = (float)(ratio[0] * height) / ratio[1]
            left = (width - new_width) / 2.0
            right = right - (width - new_width) / 2.0
    img_crop = img.crop((int(floor(left)), int(floor(upper)), int(ceil(right)), int(ceil(lower))))
    img_crop.save(filename)


def check_facebookid(facebookID):
    list_activity = Activity.objects.filter(facebookID=facebookID)
    return True if len(list_activity) > 0 else False


def read_data(feed_data):
    for entry in feed_data:
        flag_image = True
        facebookID = entry['id'].split('_')[-1]
        imageURL = ""
        altString = ""
        imageLinkURL = ""
        if check_facebookid(facebookID):
            return True

        if entry['type'] == 'photo':
            title = entry['name'] if 'name' in entry else 'Digital Green'
            if 'message' in entry:
                textContent = entry['message']
            elif 'caption' in entry:
                textContent = entry['caption']
            elif 'story' in entry:
                textContent = entry['story']
            else:
                continue
            if 'picture' in entry:
                try:
                    picture = entry['picture'].replace('_s', '_n')
                    imageURL = "\\media\\assets\\images\\facebook_uploads\\" + facebookID + "." + picture.split('.')[-1]
                    urllib.urlretrieve(picture, PROJECT_PATH + imageURL)
                    img = Image.open(PROJECT_PATH + imageURL)
                    crop_thumbnail(img, (4, 3), PROJECT_PATH + imageURL)
                    altString = "Digital Green Facebook Feed"
                    imageLinkURL = entry['link'] if 'link' in entry else "#"
                except:
                    flag_image = False
            else:
                flag_image = False
        elif (entry['type'] == 'link' or entry['type'] == 'video'):
            title = entry['name'] if 'name' in entry else 'Digital Green Shared ' + entry['type'].title()
            if 'message' in entry:
                textContent = entry['message']
            elif 'description' in entry:
                textContent = entry['description']
            else:
                continue
            if 'picture' in entry:
                try:
                    picture = urllib2.unquote(entry['picture']).split('url=')[-1]
                    imageURL = "\\media\\assets\\images\\facebook_uploads\\" + facebookID + "." + (picture.split('.')[-1])[:3]
                    urllib.urlretrieve(picture, PROJECT_PATH + imageURL)
                    img = Image.open(PROJECT_PATH + imageURL)
                    crop_thumbnail(img, (4, 3), PROJECT_PATH + imageURL)
                    altString = "Digital Green Facebook Feed"
                    imageLinkURL = entry['link'] if 'link' in entry else "#"
                except:
                    flag_image = False
            else:
                flag_image = False
        else:
            continue
        date = entry['created_time'].split('T')[0]
        avatarURL = '\\media\\assets\\images\\favicon-white.png'
        newsFeed = 1
        store_data(title, date, textContent, avatarURL, newsFeed, imageURL, altString, imageLinkURL, facebookID, flag_image)
    return False


def store_data(title, date, textContent, avatarURL, newsFeed, imageURL, altString, imageLinkURL, facebookID, flag_image):
    try:
        if flag_image:
            image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
            image_spec_entry.save()
        if(title == 'Digital Green' or title == 'Timeline Photos'):
            activity_entry = Activity(title=title, date=date, textContent=textContent, avatarURL=avatarURL, newsFeed=newsFeed, facebookID=facebookID)
            activity_entry.save()
            if flag_image:
                activity_entry.images.add(image_spec_entry)
                activity_entry.save()
        else:
            activity = Activity.objects.get(title=title)
            if flag_image:
                activity.images.add(image_spec_entry)
                activity.facebookID = facebookID
                activity.save()
    except:
        try:
            activity_entry = Activity(title=title, date=date, textContent=textContent, avatarURL=avatarURL, newsFeed=newsFeed, facebookID=facebookID)
            activity_entry.save()
            if flag_image:
                activity_entry.images.add(image_spec_entry)
                activity_entry.save()
        except:
            print ("error in saving")


TOKEN_URL = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=' + APP_ID_FACEBOOK + '&client_secret=' + APP_SECRET_FACEBOOK
response = urllib2.urlopen(TOKEN_URL)
TOKEN = response.read()
RESPONSE_URL = 'https://graph.facebook.com/digitalgreenorg/feed?' + TOKEN
response = urllib2.urlopen(RESPONSE_URL)
while(True):
    data = json.loads((response.read()))
    if 'paging' in data:
        if (read_data(data['data'])): break
        RESPONSE_URL = data['paging']['next']
        response = urllib2.urlopen(RESPONSE_URL)
    else:
        break
