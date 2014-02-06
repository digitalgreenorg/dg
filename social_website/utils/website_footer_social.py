import datetime
import json
import oauth2 as oauth
import os
import urllib2

from BeautifulSoup import BeautifulSoup
from twython import Twython

from dg.settings import APP_KEY_TWITTER, APP_SECRET_TWITTER, OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER
from dg.settings import APP_KEY_LINKEDIN, APP_SECRET_LINKEDIN, OAUTH_TOKEN_LINKEDIN, OAUTH_SECRET_LINKEDIN
from dg.settings import PROJECT_PATH

class WebsiteFooter():
    def __init__(self):
        self.template_path = os.path.join(PROJECT_PATH, "templates/social_website/includes/partials", "footer_social_media.html")
        self.template = """
                                                <li><a target='_blank' href="http://www.facebook.com/digitalgreenorg">
                                                    <h4 class="social-icon icon-fb">Facebook</h4>
                                                    <h5 class="sub-text hdg-c" id="fb-likes">%s <span>Likes</span></h5>
                                                </a></li>
                                                <li><a target='_blank' href="https://twitter.com/digitalgreenorg">
                                                    <h4 class="social-icon icon-twitter">Twitter</h4>
                                                    <h5 class="sub-text hdg-c">%s <span>Followers</span></h5>
                                                </a></li>
                                                <li><a target='_blank' href="http://www.youtube.com/user/digitalgreenorg">
                                                    <h4 class="social-icon icon-youtube">You Tube</h4>
                                                    <h5 class="sub-text hdg-c">%s <span>Videos</span></h5>
                                                </a></li>
                                                <li><a target='_blank' href="http://www.linkedin.com/company/619071">
                                                    <h4 class="social-icon icon-linkedin">Linked In</h4>
                                                    <h5 class="sub-text hdg-c">%s <span>Followers</span></h5></a></li>
                                                <li><a target="_blank" href="https://plus.google.com/102360151388546073924/posts">
                                                    <h4 class="social-icon icon-gplus grid-pad-rt-tiny">Google Plus</h4>
                                                    <h5 class="sub-text hdg-c">112<span>Followers</span></h5>
                                                </a></li>
                       """
        self.facebook = 0
        self.twitter = 0
        self.linkedin = 0
        self.youtube = 0
        try:
            self.read()
        except:
            # if the file does not exist, do nothing it will be recreated during write
            pass
            
    
    def read(self):
        fo = open(self.template_path, "r")
        data = fo.read()
        fo.close()
        
        soup = BeautifulSoup(data)
        old = soup.findAll('h5')
        
        self.html = data
        self.facebook = old[0].contents[0]
        self.twitter = old[1].contents[0]
        self.youtube = old[2].contents[0]
        self.linkedin = old[3].contents[0]
    
    def write(self):
        fo = open(self.template_path, "w")
        self.html = self.template % (self.facebook, self.twitter, self.youtube, self.linkedin)
        fo.write(self.html)
        fo.close()
    
    def fetch_facebook_likes(self):
        response = urllib2.urlopen('https://graph.facebook.com/digitalgreenorg')
        data = json.loads(response.read())
        facebook_likes = data['likes']
        facebook_likes = '{:,}'.format(int(facebook_likes))
        self.facebook = facebook_likes
    
    def fetch_twitter_followers(self):
        twitter = Twython(APP_KEY_TWITTER, APP_SECRET_TWITTER,
                          OAUTH_TOKEN_TWITTER, OAUTH_TOKEN_SECRET_TWITTER)
        twitter_obj = twitter.get_followers_ids()
        twitter_followers = len(twitter_obj['ids'])
        twitter_followers = '{:,}'.format(int(twitter_followers))
        self.twitter = twitter_followers
    
    def fetch_linkedin_subscribers(self):
        url = "http://api.linkedin.com/v1/companies/619071:(id,name,num-followers)?format=json"
        consumer = oauth.Consumer(key = APP_KEY_LINKEDIN, secret = APP_SECRET_LINKEDIN)
        token = oauth.Token(key = OAUTH_TOKEN_LINKEDIN, secret = OAUTH_SECRET_LINKEDIN)
        client = oauth.Client(consumer, token)
        resp, content = client.request(url)
        data = json.loads(content)
        linkedin_followers = data["numFollowers"]
        linkedin_followers = '{:,}'.format(int(linkedin_followers))
        self.linkedin = linkedin_followers
    
    def fetch_youtube_videos(self):
        response = urllib2.urlopen('https://gdata.youtube.com/feeds/api/users/digitalgreenorg/uploads?v=2&alt=jsonc&max-results=0')
        data = json.loads(response.read())
        youtube_videos = data['data']['totalItems']
        youtube_videos = '{:,}'.format(int(youtube_videos))
        self.youtube = youtube_videos


