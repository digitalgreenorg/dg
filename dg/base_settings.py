# Django settings for dg project.
import os
from dg.settings import WEBSITE_DOMAIN

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
APPEND_SLASH = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/media/social_website/uploads/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, *MEDIA_URL.strip("/").split("/"))

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

FILE_UPLOAD_PERMISSIONS = 0644

STATIC_URL = '/media/'
STATIC_ROOT = "/static/"
STATICFILES_DIRS = (
   # Put strings here, like "/home/html/static" or "C:/www/django/static".
   # Always use forward slashes, even on Windows.
   # Don't forget to use absolute paths, not relative paths.
   os.path.join(PROJECT_PATH, 'media'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
LOGOUT_URL = '/'
PERMISSION_DENIED_URL = '/denied/'

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'mezzanine.core.middleware.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'dg.urls'

# Google ID is required for fetching the user profile image
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [ ('id', 'id'), ('picture', 'picture') ]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates/social_website'),
            os.path.join(PROJECT_PATH, 'templates/videokheti'),
            os.path.join(PROJECT_PATH, 'templates'),
            os.path.join(PROJECT_PATH, 'templates/output'),
            os.path.join(PROJECT_PATH, 'templates/static_site'),
            os.path.join(PROJECT_PATH, 'templates/farmerbook'),
            os.path.join(PROJECT_PATH, 'media/coco/app'),
            os.path.join(PROJECT_PATH, 'templates/deoanalytics'),
            os.path.join(PROJECT_PATH, 'media/'),
            os.path.join(PROJECT_PATH, 'media/analytics/'),
            os.path.join(PROJECT_PATH, 'templates/data_upload'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.static",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.tz",
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                "mezzanine.conf.context_processors.settings",
                "mezzanine.pages.context_processors.page",
                "dg.context_processors.admin_media",
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admindocs',
    #'django.contrib.comments',
    # 'corsheaders',
    'programs',
    'geographies',
    'people',
    'videos',
    'activities',
    'api',
    #'debug_toolbar',
    'output',
    'django.contrib.humanize',
    #'south',
    'farmerbook',
    'fbconnect',
    'dimagi',
    'tastypie',
    'coco',
    'social_website',
    'social.apps.django_app.default',
    'communications',
    'human_resources',
    'feeds',
    'deoanalytics',
    'data_upload',
    'raw_data_analytics',
    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.blog',
    'mezzanine.forms',
    'mezzanine.pages',
    'mezzanine.galleries',
    'mezzanine.twitter',
    'filebrowser_safe',
    'grappelli_safe',
    'videokheti',
    'ivr',
    'training',
    'loop',
    'qacoco',
    'mrppayment',
    'smart_selects',
    'loop_ivr',
    'dataexport',
    'rest_framework',
    # 3rd Party
    'django_extensions',
    #drf TokenAuthentication
    'rest_framework.authtoken',
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"
GRAPPELLI_INSTALLED = True
TESTING = True
ADMIN_MENU_COLLAPSED = False
COMMENTS_USE_RATINGS = False
COMMENTS_ACCOUNT_REQUIRED  = True
RICHTEXT_FILTER_LEVEL = 2
BLOG_USE_FEATURED_IMAGE = True
#ADMIN_REMOVAL = []
#following line makes sessionid cookie accessible to in-browser javascript
SESSION_COOKIE_HTTPONLY = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'media/social_website/uploads/log/logfile'),
            'formatter': 'standard',
        },
        'ap_migration_log': {
            'level': 'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, '../geographies/management/commands/log/ap_migration_log'),
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'api_access_log': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, '../api/log/logfile'),
            'formatter': 'standard',
        },

    },
    'loggers': {
        'social_website': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'dashboard': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'loop_ivr': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'geographies': {
            'handlers': ['ap_migration_log'],
            'level' : 'INFO',
        },
        'coco_api':{
            'handlers': ['api_access_log'],
            'level': 'INFO',
        }
    }
}

PRODUCT_PAGE = ('%s%s')%(WEBSITE_DOMAIN, 'solutions/')
LOOP_PAGE = ('%s%s')%(WEBSITE_DOMAIN, 'loop/')
COCO_PAGE = ('%s%s')%(WEBSITE_DOMAIN, 'coco/')
TRAINING_PAGE = ('%s%s')%(WEBSITE_DOMAIN, 'training/')
VIDEOS_PAGE = ('%s%s')%(WEBSITE_DOMAIN, 'videos/')
LOOP_APP_PAGE = ('%s')%('https://play.google.com/store/apps/details?id=loop.org.digitalgreen.loop')
TRAINING_APP_PAGE = ('%s')%('https://play.google.com/store/apps/details?id=org.digitalgreen.trainingapp')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [        
        'rest_framework.permissions.IsAuthenticated', 
    ],
}