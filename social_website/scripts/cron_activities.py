from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
import pickle
from dashboard.models import Screening, ServerLog, Village
from social_website.models import Partner
from social_website.scripts.generate_activities import add_milestone, add_village

for partner in Partner.objects.all()[1:2]:
    print partner.uid
    add_milestone(partner)

# adding village activity
file = "".join([dg.settings.MEDIA_ROOT, "village_partner_list.p"])
village_partner_list = pickle.load(open(file, "rb"))
villages = Village.objects.all()
for village in villages:
    partners = list(set(Screening.objects.filter(village=village).values_list('user_created__cocouser__partner', flat=True)))
    for partner_id in partners:
        partner = Partner.objects.get(coco_id=partner_id)
        if (village.id, partner.uid) not in village_partner_list:
            add_village(village, partner)
        else:
            print(village.village_name)


