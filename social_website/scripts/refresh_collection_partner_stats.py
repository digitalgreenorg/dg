from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from social_website.migration_functions import populate_collection_stats, populate_partner_stats
from social_website.models import Collection, Partner

for collection in Collection.objects.all():
    populate_collection_stats(collection)
    
for partner in Partner.objects.all():
    populate_partner_stats(partner)
    