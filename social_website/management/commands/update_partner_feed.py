import logging
import pickle
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from dashboard.models import Partners, Screening, ServerLog, Village
from dg.settings import MEDIA_ROOT
from social_website.models import Activity, Partner
from social_website.utils.generate_activities import ActivityType, add_milestone, add_village

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.update_partner_feed()
    
    def update_partner_feed(self):
        logger = logging.getLogger('social_website')
        for partner in Partner.objects.all():
            try:
                Partners.objects.get(id=partner.coco_id)
            except:
                continue
            types = [ActivityType.video_milestone, ActivityType.village_milestone, ActivityType.screening_milestone, ActivityType.viewer_milestone]
            initial_rows = len(Activity.objects.filter(partner=partner, type__in=types))
            add_milestone(partner)
            final_rows = len(Activity.objects.filter(partner=partner, type__in=types))
            logger.info("%s Rows Added: %s" % (partner.name, final_rows - initial_rows))

        # adding village activity
        file = "".join([MEDIA_ROOT, "village_partner_list.p"])
        village_partner_list = pickle.load(open(file, "rb"))
        initial = len(village_partner_list)
        villages = Village.objects.all()
        initial_rows = len(Activity.objects.filter(type=ActivityType.new_village))
        for village in villages:
            partners = list(set(Screening.objects.filter(village=village).values_list('user_created__cocouser__partner', flat=True)))
            for partner_id in partners:
                try:
                    partner = Partner.objects.get(coco_id=partner_id)
                except Partner.DoesNotExist:
                    continue 
                if (village.id, partner.uid) not in village_partner_list:
                    add_village(village, partner)
        village_partner_list = pickle.load(open(file, "rb"))
        final = len(village_partner_list)
        final_rows = len(Activity.objects.filter(type=ActivityType.new_village))
        logger.info("Rows to be Added: %s" % (final - initial))
        logger.info("Rows Added: %s" % (final_rows - initial_rows))
