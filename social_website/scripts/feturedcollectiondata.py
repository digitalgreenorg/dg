import site, sys
sys.path.append(r'C:\Users\Aadish\Documents\dg')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from social_website.models import *


featured_collection_dict = {
                            'Bhili': '203',
                            'Gondi': '194',
                            'Hindi': '18',
                            'Ho': '40',
                            'Kannada': '79',
                            'Mundari': '34',
                            'Narsinghpuria': '199',
                            'Neemadi': '92',
                            'Oriya': '152',
                            'Sadri': '143',
                            'Santhali': '192',
                            'Telugu': '116',
                            'Thethi': '114',
                            }

count = 1
for key in featured_collection_dict:
    language_obj = Language.objects.get(name=key)
    fc_object = FeaturedCollection(uid=count, language=language_obj, collection=featured_collection_dict[key],
                                   collageURL='/media/assets/images/Collage/Collection ID '+featured_collection_dict[key]+'.jpg')
    fc_object.save()
    count += 1