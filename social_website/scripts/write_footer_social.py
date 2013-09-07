import datetime
import httplib
import json
import oauth2 as oauth
import urllib2

from BeautifulSoup import BeautifulSoup
from twython import Twython, exceptions

from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from dg.settings import APP_KEY_TWITTER, APP_SECRET_TWITTER, OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER
from dg.settings import APP_KEY_LINKEDIN, APP_SECRET_LINKEDIN, OAUTH_TOKEN_LINKEDIN, OAUTH_SECRET_LINKEDIN

fo = open(dg.settings.PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "r")
data = fo.read()
fo.close()

log = open(dg.settings.MEDIA_ROOT+ "/log/footer_log.txt", "a")
log.write(str(datetime.datetime.utcnow()) + '\n')
soup = BeautifulSoup(data)
old = soup.findAll('h5')

old_fb = old[0].contents[0]
old_twitter = old[1].contents[0]
old_yt = old[2].contents[0]
old_linkdin = old[3].contents[0]

# Facebook Likes
try:
    response = urllib2.urlopen('https://graph.facebook.com/digitalgreenorg')
    data = json.loads(response.read())
    facebook_likes = data['likes']
    facebook_likes = '{:,}'.format(int(facebook_likes))
except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
    facebook_likes = old_fb
    log.write("error in updating facebook likes\n")

# Twitter Followers
try:
    twitter = Twython(APP_KEY_TWITTER, APP_SECRET_TWITTER,
                      OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER)
    twitter_obj = twitter.get_followers_ids()
    twitter_followers = len(twitter_obj['ids'])
    twitter_followers = '{:,}'.format(int(twitter_followers))
except exceptions:
    twitter_followers = old_twitter
    log.write("error in updating twitter followers\n")

# Youtube Videos
try:
    response = urllib2.urlopen('https://gdata.youtube.com/feeds/api/users/digitalgreenorg/uploads?v=2&alt=jsonc&max-results=0')
    data = json.loads(response.read())
    youtube_videos = data['data']['totalItems']
    youtube_videos = '{:,}'.format(int(youtube_videos))
except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
    youtube_videos = old_yt
    log.write("error in updating youtube videos\n")

# Linkedin Followers
try:
    url = "http://api.linkedin.com/v1/companies/619071:(id,name,num-followers)?format=json"
    consumer = oauth.Consumer(key = APP_KEY_LINKEDIN, secret = APP_SECRET_LINKEDIN)
    token = oauth.Token(key = OAUTH_TOKEN_LINKEDIN, secret = OAUTH_SECRET_LINKEDIN)
    client = oauth.Client(consumer, token)
    resp, content = client.request(url)
    data = json.loads(content)
    linkedin_followers = data["numFollowers"]
    linkedin_followers = '{:,}'.format(int(linkedin_followers))
except Exception:
    linkedin_followers = old_linkdin
    log.write("error in updating linkedin followers\n")

file_template = """
                                        <li><a target='_blank' href="http://www.facebook.com/digitalgreenorg"><h4 class="social-icon icon-fb">Facebook</h4> <h5 class="sub-text hdg-c" id="fb-likes">%s <span>Likes</span></h5></a></li>
                                        <li><a target='_blank' href="https://twitter.com/digitalgreenorg"><h4 class="social-icon icon-twitter">Twitter</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n
                                        <li><a target='_blank' href="http://www.youtube.com/user/digitalgreenorg"><h4 class="social-icon icon-youtube">You Tube</h4> <h5 class="sub-text hdg-c">%s <span>Videos</span></h5></a></li>\n
                                        <li><a target='_blank' href="http://www.linkedin.com/company/619071"><h4 class="social-icon icon-linkedin">Linked In</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n
               """
file_template = file_template % (facebook_likes, twitter_followers, youtube_videos, linkedin_followers)

fo = open(dg.settings.PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "w")
fo.write(file_template)
fo.close()
log.close()