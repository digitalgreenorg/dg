import site, sys
DEBUG = True
INTERNAL_IPS = ('127.0.0.1',)
# ALLOWED_HOSTS = ['www.digitalgreen.org', '174.129.35.27', 'qacoco.digitalgreen.org', 'digitalgreen.org']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'solutions.digitalgreen.org', 'qacoco.digitalgreen.org']

# Domain of currently running server
CURRENT_DOMAIN = 'solutions.digitalgreen.org'
WEBSITE_DOMAIN = 'http://www.digitalgreen.org/' 
PRIVACY_POLICY = 'http://www.digitalgreen.org/privacy-policy/' 
TERMS_SERVICE = 'http://www.digitalgreen.org/terms-of-service/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dg_28mar18',
        'USER': 'root',
        'PASSWORD': 'root',
        #'HOST': 'production.cvoutccpkcep.us-east-1.rds.amazonaws.com',
        'HOST': 'localhost',
        'PORT' : 3306,
    }
}

# Elastic search indices
BASE_INDEX = 'dg'
FACET_INDEX = BASE_INDEX  + '_facet_index' 
COMPLETION_INDEX = BASE_INDEX  + '_completion_index'
VIDEO_INDEX = BASE_INDEX  + '_video_index'

MEDIA_ROOT = '~/Documents/dg/dg/media/social_website/uploads/' 

STATIC_DOC_ROOT = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#^-+@st9^02l+@651*-=!)9fey*gj82roi91#^0qi=@sk)l3hv'

# Twitter API Keys
# DG Account
# Username: digitalgreenorg 
APP_KEY_TWITTER = 'DQQXdUTET5sm7mlFwlTW7A'
APP_SECRET_TWITTER = 'VSYSKHCYlzcedjhq7Wg87rYib83Rnsdsj28PR2QtDI'
OAUTH_TOKEN_TWITTER = '86273857-lWVBEkfUTd3Mfw0qsZ4LrNsYn9Ss81YIYJJKGy31U'
OAUTH_TOKEN_SECRET_TWITTER = 'ipuYXjY9byDoF3mswUnjvlsehUV2pet2KJ7yMPKw'

# LinkedIn API Keys
# DG Development Application
# Admins and developers: rikin@digitalgreen.org, nandini@digitalgreen.org, aadish@digitalgreen.org
APP_KEY_LINKEDIN = '8kdv5oky0zcs'
APP_SECRET_LINKEDIN = 'vKWWkyIcM2ESpnz6'
OAUTH_TOKEN_LINKEDIN = 'de6d6cfe-b9f6-4d0c-b8e4-bb32c9e99d05'
OAUTH_SECRET_LINKEDIN = 'a972cf12-b203-4b70-85b4-b2a7a4040023'

# Facebook API Keys
# DG Facebook Development Account
# Email: games@digitalgreen.org
SOCIAL_AUTH_FACEBOOK_KEY = '149405231925556'
SOCIAL_AUTH_FACEBOOK_SECRET = '4063b3dbbf1fc0ee6a83954d54f0880a'

# Google API Keys
# DG Google Development Application
# Email: admin@digitalgreen.org
#Old Google Auth Credentials
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '84137409430-cm1j7a2bsc7gqi0a0ebs6cvc97gmj55p.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'fH3kbre-_3FG_bg7MumZXReO'
#GOOGLE_API_KEY = 'AIzaSyCte0s5uccnHEnpXF_SqV93BytBOr008Tk'

# Email: sourabh@digitalgreen.org
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '679192854070-q2e5dqp6v1fj9v4k50q4d3lqd7t4s8rd.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'O6ISp8oYjelAh86ONBmVMFmU'

# New Google Auth Credentials
# Email: server@digitalgreen.org
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1032200188669-opa8vb8nqqi1kclrf4sgfcbiani1rrm0.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'gd7qo1s1pFIxElJdG_eE3u1O'
# Email: admin@digitalgreen.org
GOOGLE_API_KEY = 'AIzaSyCte0s5uccnHEnpXF_SqV93BytBOr008Tk'

# Dimagi Credentials
DIMAGI_USERNAME = 'jahnavi@digitalgreen.org'
DIMAGI_PASSWORD = 'Dravid19'

# Exotel Credentials
EXOTEL_ID = 'digitalgreen3'
EXOTEL_TOKEN = '7fcbc010698716d837be0239452c6e3095c67805'   
EXOTEL_HELPLINE_NUMBER = '01139595953'
NO_EXPERT_GREETING_APP_ID = '124538'
OFF_HOURS_GREETING_APP_ID = '124897'
OFF_HOURS_VOICEMAIL_APP_ID = '125014'
BROADCAST_APP_ID = '131151'

# Text Local Credentials
TEXTLOCAL_API_KEY = 'RUKWkzm2cvM-2ZNJE413TY5xGKt3m1eNpy4hNYImL4'

team_contact = ['09205812770', '09971615435', '07633863787', '09891256494', '09013623264', '09810188735', '09810981216']

#Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'server@digitalgreen.org'
EMAIL_HOST_PASSWORD = 'dgserver@123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

S3_ACCESS_KEY = '01GE4NJEXRFQTBCFG782'
S3_SECRET_KEY = 'bK8gt4siHBryH/cRagSMtcDPwNbfB0l2E/KXVhYy'

#New S3 Accounts Keys
ACCESS_KEY = 'AKIAJZYOLHFWPSD57FKQ'
SECRET_KEY = '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'
YOUTUBE_SIMPLE_ACCESS = 'AIzaSyCte0s5uccnHEnpXF_SqV93BytBOr008Tk'
#For cron scripts
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')

try:
    from base_settings import *
except ImportError:
    pass

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

#import logging
#logging.basicConfig(
#    level = logging.INFO,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = '/tmp/djangoLogProd.log',)