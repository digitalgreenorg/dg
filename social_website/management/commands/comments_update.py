from django.core.management.base import BaseCommand, CommandError

from activities.models import Screening
from people.models import Animator
from social_website.models import Comment
from social_website.migration_functions import update_questions_asked, populate_animators

class Command(BaseCommand):
    ''' One time script to migrate comments from pma to screening, populate animator '''

    def handle(self, *args, **options):

        # Deleting all previous comments mapped to persons
        Comment.objects.all().delete()

        # Populate Animator table
        animators = Animator.objects.all()
        for obj in animators:
            populate_animators(obj)

        # Populate Comments from Screenings
        try:
            count = 1
            screenings = Screening.objects.all()
            for obj in screenings:
                update_questions_asked(obj)
                count += 1
            print count     
        except Exception as e:
            print e
