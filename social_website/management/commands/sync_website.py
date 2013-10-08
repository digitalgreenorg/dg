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

from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from social_website.utils.refresh_stats import refresh_collection_partner_stats, refresh_offline_stats, refresh_online_stats
from social_website.utils.elastic_search.setup import setup_elastic_search
from social_website.utils.sync_with_coco import recreate_person_video_record, sync_with_serverlog


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-c', '--complete',
                    action='store_true',
                    default=False,
                    help='Syncs the website with COCO stats, serverlog  and youtube stats and setup elastic search with latest stats'),
        make_option('-o', '--only_offline',
                    action='store_true',
                    default=False,
                    help='Syncs website with COCO stats, serverlog and steup elastic search'),
        make_option('-n', '--only_online',
                    action='store_true',
                    default=False,
                    help='Syncs website videos with latest youtube stats and setup elastic search'),
        make_option('-f', '--fast',
                    action='store_true',
                    default=False,
                    help='Sync website with serverlog and setup elastic search'),
        )

    def complete(self):
        recreate_person_video_record()
        sync_with_serverlog()
        refresh_offline_stats()
        refresh_online_stats()
        refresh_collection_partner_stats()
        setup_elastic_search()

    def only_offline(self):
        recreate_person_video_record()
        sync_with_serverlog()
        refresh_offline_stats()
        refresh_collection_partner_stats()
        setup_elastic_search()

    def only_online(self):
        refresh_online_stats()
        refresh_collection_partner_stats()
        setup_elastic_search()

    def fast(self):
        sync_with_serverlog()
        refresh_collection_partner_stats()
        setup_elastic_search()

    def handle(self, *args, **options):
        if options['complete']:
            self.complete()
        elif options['only_offline']:
            self.only_offline()
        elif options['only_online']:
            self.only_online()
        elif options['fast']:
            self.fast()
        else:
            if datetime.utcnow().weekday() % 2:
                self.complete()
            else:
                self.fast()

