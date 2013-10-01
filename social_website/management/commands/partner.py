from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from social_website.scripts.cron_activities import call_partner_activities


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all',
                    action='store_true',
                    default=True,
                    help='Populate partner activities and milestones'),
        )

    def handle(self, *args, **options):
        if (options['all']):
            call_partner_activities()
