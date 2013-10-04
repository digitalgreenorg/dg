from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from scripts.youtube_utils import call_youtube_update
from social_website.utils.refresh_stats import refresh_online_stats, call_refresh_stats
from social_website.utils.elastic_search.setup import call_setup_elastic
from social_website.utils.sync_with_coco import sync_website_with_coco

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
        do_all = False
        if options['all']:
            do_all = True
        if do_all or options['update_youtube']:
            if len(args):
                if (args[0] == 'full'):
                    call_youtube_update(True)
                else:
                    print ''' "full" needs to be provided as argument to run for all videos with youtube id'''
            else:
                call_youtube_update()
        if do_all or options['website_sync']:
            sync_website_with_coco()
        if do_all or options['online_stats']:
            refresh_online_stats()
        if do_all or options['offline_stats']:
            refresh_offline_stats()
        if do_all or options['refresh_stats']:
            refresh_collection_partner_stats()
        if do_all or options['setup_elastic']:
            call_setup_elastic()
    
'''
    COMPLETE
    recreate_person_video_record slow
    sync_website_with_coco fast
    refresh_offline_stats fast
    refresh_online_stats slow
    refresh_collection_partner fast
    setup_elastic_search
    
    Only OFFLINE
    recreate_person_video_record slow
    sync_website_with_coco fast
    refresh_offline_stats fast
    refresh_collection_partner fast
    setup_elastic_search
    
    Only Online
    refresh_online_stats slow
    refresh_collection_partner fast
    setup_elastic_search
    
    FAST
    sync_website_with_coco fast
    refresh_collection_partner fast
    setup_elastic_search
    
    DEFAULT
    if utcnow().weekday() % 2
        complete
    else 
        fast
'''

    
    
    
    
    
    
