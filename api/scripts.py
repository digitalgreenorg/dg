# app
from api.views import CreateView
from api.models import View
from django.contrib.auth.models import Group
# view
from activities.views import ScreeningAPIView
from geographies.views import VillageAPIView, BlockAPIView, DistrictAPIView, StateAPIView, CountryAPIView

'''
How to run this script?
Here's how: 
1.) Open this project folder in a terminal
2.) Activate the required environment to run this project
3.) Run the following command in the terminal:
    python manage.py shell
4.) Now you'll be able to see the IPython console
5.) Run the following command in the terminal:
    %run api/scripts.py
6.) If you get any location errors, then try to check the current folder using pwd command
'''

def createAView(view_class):
    '''
    This function adds a view to the database
    '''
    view = View(view_name = view_class)
    view.save()
    return


def addAGroupByName(view_class_name, group_name):
    '''
    This function adds a group to a view by view name to the database
    '''
    view = View.objects.get(view_name=view_class_name)
    gr = Group.objects.get(name=group_name)
    view.permission_groups.add(gr)
    view.save()   
    return 


def addAGroupByID(view_id, group_id):
    '''
    This function adds a group to a view by view name to the database
    '''
    view = View.objects.get(id__exact=view_id)
    gr = Group.objects.get(id__exact=group_id)
    view.permission_groups.add(gr)
    view.save()   
    return 


def addAGroupByViewID(view_id, group_name):
    '''
    This function adds a group to a view by view id to the database
    '''
    view = View.objects.get(id__exact=view_id)
    gr = Group.objects.get(name=group_name)
    view.permission_groups.add(gr)
    view.save()   
    return 


def addAGroupByGroupID(view_class_name, group_id):
    '''
    This function adds a group to a view by view name to the database
    '''
    view = View.objects.get(view_name=view_class_name)
    gr = Group.objects.get(id__exact=group_id)
    view.permission_groups.add(gr)
    view.save()   
    return 


if __name__=="__main__":
    '''
    This function is available to be edited according to the required view to be added in the database
    '''
    # # to add a single view
    # view_class = VillageAPIView.__name__
    # createAView(view_class)


    # # to add a group to a view by view name
    # group_name = "coco_api_access"
    # addAGroupByName(view_class, group_name)


    # # to add a group to a view by view id
    # group_name = "coco_api_access"
    # addAGroupByID(view_id, group_name)


    # # to create multiple views and assign a group
    view_class_list = [DistrictAPIView.__name__, BlockAPIView.__name__]
    group_id = 20
    for view in view_class_list:
        createAView(view)
        addAGroupByGroupID(view, group_id)


    # # to add multiple views belonging to multiple groups
    # permission map for views and allowed user groups
    PERMISSIONS_MAP = {
        'ScreeningAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'DefaultView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'VillageAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'BlockAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'DistrictAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'StateAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'CountryAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'FarmersJsonAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS', 'AWAAZDE_Group' ],
        'FarmersCsvAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'PartnerAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'ProjectAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'VideoAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
        'CreateView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    }

    # for key in PERMISSIONS_MAP.keys():
    #     view_name = key
    #     group_list = PERMISSIONS_MAP[key]
    #     for group_name in group_list:
    #         createAView(view)
    #         addAGroupByName(view_name, group_name)

