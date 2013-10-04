import logging
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from social_website.utils.website_footer_social import WebsiteFooter
from social_website.scripts.activity_facebook_data import get_facebook_feed

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
                    action='store_true',
                    default=False,
                    help='Update news feed and footer statistics'),
        make_option('-f', '--footer',
                    action='store_true',
                    default=False,
                    help='Update footer statistics'),
        make_option('-n', '--newsfeed',
                    action='store_true',
                    default=False,
                    help='Update news feed from Facebook'),
        )

    def handle(self, *args, **options):
        if (options['all']):
            self.update_footer_stats()
            get_facebook_feed()
        if (options['footer']):
            self.update_footer_stats()
        if (options['newsfeed']):
            get_facebook_feed()

    
    def update_footer_stats(self):
        logger = logging.getLogger('social_website')    
        footer = WebsiteFooter()
        try:
            footer.fetch_facebook_likes()
        except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            logger.error("error in updating facebook likes")
        try:
            footer.fetch_twitter_followers()
        except exceptions:
            logger.error("error in updating twitter followers")
        try:
            footer.fetch_youtube_videos()
        except (httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            logger.error("error in updating youtube videos")
        try:
            footer.fetch_linkedin_subscribers()
        except Exception:
            logger.error("error in updating linkedin subscribers")
        footer.write()
        logger.info("Updated footer stats")
