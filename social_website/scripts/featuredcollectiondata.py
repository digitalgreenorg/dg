import site, sys
sys.path.append('/home/ubuntu/code/dg_test')
site.addsitedir('/home/ubuntu/.virtualenv/dg_testbed/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)
from social_website.models import Collection, FeaturedCollection


featured_collection_dict = {
                            'Bhili': 114,
                            'Gondi': 122,
                            'Hindi': 31,
                            'Ho': 57,
                            'Kannada': 43,
                            'Mundari': 39,
                            'Narsinghpuria': 116,
                            'Neemadi': 73,
                            'Oriya': 104,
                            'Sadri': 126,
                            'Santhali': 174,
                            'Telugu': 97,
                            'Thethi': 89,
                            }

for key in featured_collection_dict:
    collection = Collection.objects.get(uid = featured_collection_dict[key])
    fc_object = FeaturedCollection(collection = collection,
                                   collageURL='/media/assets/images/Collage/Collection ' + collection.language + '.jpg')
    fc_object.save()
