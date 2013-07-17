import site, sys
sys.path.append('/home/ubuntu/code/dg_test')
site.addsitedir('/home/ubuntu/.virtualenv/dg_testbed/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import json, urllib2
from twython import *
from linkedin import linkedin
import settings
setup_environ(settings)
from base_settings import PROJECT_PATH
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
authentication = linkedin.LinkedInDeveloperAuthentication(APP_KEY_LINKEDIN,
                                                          APP_SECRET_LINKEDIN,
                                                          OAUTH_TOKEN_LINKEDIN,
                                                          OAUTH_SECRET_LINKEDIN,
                                                          "", linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)
linkedin_followers = application.get_companies(company_ids=[619071],selectors=['num-followers'])['values'][0]['numFollowers']
linkedin_followers = '{:,}'.format(int(linkedin_followers))

fo = open(PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "r")
data = fo.readlines()
fo.close()

data[0] = """							<li><a href="http://www.facebook.com/digitalgreenorg"><h4 class="social-icon icon-fb">Facebook</h4> <h5 class="sub-text hdg-c" id="fb-likes">%s <span>Like</span></h5></a></li>\n""" % facebook_likes
data[1] = """							<li><a href="https://twitter.com/digitalgreenorg"><h4 class="social-icon icon-twitter">Twitter</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n""" % twitter_followers
data[2] = """							<li><a href="http://www.youtube.com/user/digitalgreenorg"><h4 class="social-icon icon-youtube">You Tube</h4> <h5 class="sub-text hdg-c">%s <span>Videos</span></h5></a></li>\n""" % youtube_videos
data[3] = """							<li><a href="http://www.linkedin.com/company/619071"><h4 class="social-icon icon-linkedin">Linked In</h4> <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>\n""" % linkedin_followers

fo = open(PROJECT_PATH+"/templates/social_website/includes/partials/footer_social_media.html", "w")
fo.writelines( "%s" % line for line in data )
fo.close()
