# django imports
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, call_command
# csv imports
import unicodecsv as csv
# app imports
from api.views import CreateView
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

# mapping of view class with group permitted to access it
PERMISSIONS_MAP = {
    ScreeningAPIView.__name__: ['cocoadmin','api_access' ],
    VillageAPIView.__name__: ['cocoadmin','api_access' ],
    BlockAPIView.__name__: ['cocoadmin','api_access' ],
    DistrictAPIView.__name__: ['cocoadmin','api_access' ],
    StateAPIView.__name__: ['cocoadmin','api_access' ],
    CountryAPIView.__name__: ['cocoadmin','api_access' ],
    GeoInfoView.__name__: ['cocoadmin','api_access' ],
    FarmersJsonAPIView.__name__: ['cocoadmin','api_access', 'AWAZDE'],
    FarmersCsvAPIView.__name__: ['cocoadmin','api_access', 'AWAZDE' ],
    FarmerInfoView.__name__: ['cocoadmin','api_access' ],
    PartnerAPIView.__name__: ['cocoadmin','api_access' ],
    ProjectAPIView.__name__: ['cocoadmin','api_access' ],
    VideoAPIView.__name__: ['cocoadmin','api_access' ]
}

class CreateViewAndAddGroups(self):
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
		# error_file = open('/home/ubuntu/code/dg_git/api/management/commands/errors.csv', 'wb')
		# wrtr = csv.writer(error_file, delimiter=',', quotechar='"')
        createAdd = CreateViewAndAddGroups()
        for key in PERMISSIONS_MAP.keys():
            view_name = key
            group_list = PERMISSIONS_MAP[key]
            for group_name in group_list:
                try:
                    createAdd.createAView(view_name)
                    createAdd.addAGroupByName(view_name, group_name)
                except Exception as e:
                    wrtr.writerow([key, "**insertion-error**", group_name), e])
                    print(e, "**insertion-error")
		
		# error_file.close()
