import json
import oauth2 as oauth
import site
import sys
import urllib2

from twython import Twython

from django.core.management import setup_environ
import settings
setup_environ(settings)

from settings import APP_KEY_TWITTER, APP_SECRET_TWITTER, OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER
from settings import APP_KEY_LINKEDIN, APP_SECRET_LINKEDIN, OAUTH_TOKEN_LINKEDIN, OAUTH_SECRET_LINKEDIN

# Facebook Likes
response = urllib2.urlopen('https://graph.facebook.com/digitalgreenorg')
data = json.loads(response.read())
facebook_likes = data['likes']
facebook_likes = '{:,}'.format(int(facebook_likes))

# Twitter Followers 
twitter = Twython(APP_KEY_TWITTER, APP_SECRET_TWITTER,
                  OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER)
twitter_obj = twitter.get_followers_ids()
twitter_followers = len(twitter_obj['ids'])
twitter_followers = '{:,}'.format(int(twitter_followers))

# Youtube Videos
response = urllib2.urlopen('https://gdata.youtube.com/feeds/api/users/digitalgreenorg/uploads?v=2&alt=jsonc&max-results=0')
data = json.loads(response.read())
youtube_videos = data['data']['totalItems']
youtube_videos = '{:,}'.format(int(youtube_videos))

# Linkedin Followers
url = "http://api.linkedin.com/v1/companies/619071:(id,name,num-followers)?format=json"
consumer = oauth.Consumer(key = APP_KEY_LINKEDIN, secret = APP_SECRET_LINKEDIN)
token = oauth.Token(key = OAUTH_TOKEN_LINKEDIN, secret = OAUTH_SECRET_LINKEDIN)
client = oauth.Client(consumer, token)
resp, content = client.request(url)
data = json.loads(content)
linkedin_followers = data["numFollowers"]
linkedin_followers = '{:,}'.format(int(linkedin_followers))

fo = open(settings.PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "r")
data = fo.readlines()
fo.close()

file_template = """                            
                                        <li><a href="http://www.facebook.com/digitalgreenorg"><h4 class="social-icon icon-fb">Facebook</h4> <h5 class="sub-text hdg-c" id="fb-likes">%s <span>Like</span></h5></a></li>
                                        <li><a href="https://twitter.com/digitalgreenorg"><h4 class="social-icon icon-twitter">Twitter</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n
                                        <li><a href="http://www.youtube.com/user/digitalgreenorg"><h4 class="social-icon icon-youtube">You Tube</h4> <h5 class="sub-text hdg-c">%s <span>Videos</span></h5></a></li>\n
                                        <li><a href="http://www.linkedin.com/company/619071"><h4 class="social-icon icon-linkedin">Linked In</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n
               """
file_template = file_template % (facebook_likes, twitter_followers, youtube_videos, linkedin_followers)

fo = open(settings.PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "w")
fo.write(file_template)
fo.close()