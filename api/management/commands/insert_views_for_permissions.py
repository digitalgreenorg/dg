# django imports
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
# csv imports
import unicodecsv as csv
# app imports
from api.models import View
from activities.views import ScreeningAPIView
from geographies.views import VillageAPIView, BlockAPIView, DistrictAPIView, StateAPIView, CountryAPIView, GeoInfoView
from people.views import FarmersJsonAPIView, FarmersCsvAPIView, FarmerInfoView
from programs.views import PartnerAPIView, ProjectAPIView
from videos.views import VideoAPIView

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

# add a view in this list to insert it in database
VIEWS_LIST = {
    ScreeningAPIView.__name__,
    VillageAPIView.__name__,
    BlockAPIView.__name__,
    DistrictAPIView.__name__,
    StateAPIView.__name__,
    CountryAPIView.__name__,
    GeoInfoView.__name__,
    FarmersJsonAPIView.__name__,
    FarmersCsvAPIView.__name__,
    FarmerInfoView.__name__,
    PartnerAPIView.__name__,
    ProjectAPIView.__name__,
    VideoAPIView.__name__,
}

class CreateViewAndAddGroups():
    """
    Class to create views and add groups for View model
    """

    def createAView(self, view_class):
        '''
        This function adds a view to the database
        '''

        view = View(view_name = view_class)
        view.save()
        return

    def addAGroupByName(self, view_class_name, group_name):   
        '''
        This function adds a group to a view by view name to the database
        '''

        view = View.objects.get(view_name=view_class_name)
        gr = Group.objects.get(name=group_name)
        view.permission_groups.add(gr)
        view.save()   
        return 


class Command(BaseCommand):
    """
    This class is used to add management commands to insert views in the database
    """
    
    def handle(self, *args, **options):
        prod_path = '/home/ubuntu/code/dg_git/api/management/commands/errors.csv'
        local_path = '/Users/stuti/Desktop/dg/api/management/commands/errors.csv'
        error_file = open(local_path, 'wb')
        wrtr = csv.writer(error_file, delimiter=',', quotechar='"')
        createAdd = CreateViewAndAddGroups()

        for (i, view_name) in enumerate(VIEWS_LIST):
            try:
                createAdd.createAView(view_name)
                # createAdd.addAGroupByName(view_name, "cocoadmin")
            except Exception as e:
                wrtr.writerow([i, "**insertion-error**", view_name, e])
                print(e, "**insertion-error")
		
        error_file.close()
