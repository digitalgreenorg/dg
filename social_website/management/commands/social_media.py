from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from social_website.scripts.write_footer_social import call_footer_stats
from social_website.scripts.activity_facebook_data import get_facebook_feed


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
                    action='store_true',
                    default=False,
                    help='Update news feed and footer statistics'),
        make_option('-f', '--footer_statistics',
                    action='store_true',
                    default=False,
                    help='Update footer statistics'),
        make_option('-n', '--news_feed',
                    action='store_true',
                    default=False,
                    help='Update news feed from facebook feed'),
        )

    def handle(self, *args, **options):
        if (options['all']):
            call_footer_stats()
            get_facebook_feed()
        if (options['footer_statistics']):
            call_footer_stats()
        if (options['news_feed']):
            get_facebook_feed()

