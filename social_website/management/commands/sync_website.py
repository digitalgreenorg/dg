from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from social_website.scripts.website_sync import call_website_sync
from social_website.scripts.refresh_collection_partner_stats import refresh_online_stats, call_refresh_stats
from scripts.update_video_duration_from_youtube import call_youtube_update
from social_website.scripts.setup_elastic_search import call_setup_elastic


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
                    action='store_true',
                    default=False,
                    help='Run all the cron jobs to sync website with COCO'),
        make_option('-y', '--update_youtube',
                    action='store_true',
                    default=False,
                    help='''Run you_tube script to upload images to S3 and fetch video duration
                            Provide "full" as argument if want to run for all videos with youtube id'''),
        make_option('-w', '--website_sync',
                    action='store_true',
                    default=False,
                    help='Fetch Stats from COCO and Server Log in Website tables'),
        make_option('-r', '--refresh_stats',
                    action='store_true',
                    default=False,
                    help='Refresh partner and collection stats'),
        make_option('-e', '--setup_elastic',
                    action='store_true',
                    default=False,
                    help='Set up elastic search with latest data'),
        make_option('-o', '--online_stats',
                    action='store_true',
                    default=False,
                    help='Refreshes the Online Likes(Youtube + Website) and Online Views'),
        )

    def handle(self, *args, **options):
        if (options['all']):
            call_youtube_update()
            call_website_sync()
            call_refresh_stats()
            call_setup_elastic()
        if (options['update_youtube']):
            if len(args):
                if (args[0] == 'full'):
                    call_youtube_update(True)
                else:
                    print ''' "full" needs to be provided as argument to run for all videos with youtube id'''
            else:
                call_youtube_update()
        if (options['website_sync']):
            call_website_sync()
        if (options['refresh_stats']):
            call_refresh_stats()
        if (options['setup_elastic']):
            call_setup_elastic()
        if (options['online_stats']):
            refresh_online_stats()
