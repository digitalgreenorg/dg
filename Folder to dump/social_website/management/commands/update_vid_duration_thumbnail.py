from django.core.management.base import BaseCommand

from libs.youtube_utils import call_youtube_update


class Command(BaseCommand):
    help = '''Run you_tube script to upload images to S3 and fetch video duration
              Provide "full" as argument if want to run for all videos with youtube id'''

    def handle(self, *args, **options):
        if len(args):
            if (args[0] == 'full'):
                call_youtube_update(True)
            else:
                print ''' "full" needs to be provided as argument to run for all videos with youtube id'''
        else:
            call_youtube_update()