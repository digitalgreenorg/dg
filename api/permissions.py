# rest framework imports
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
# app imports
from api.models import View
# logging imports
import logging

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"      

logger = logging
logger = logging.getLogger('coco_api')

class IsAllowed(permissions.BasePermission):
    """
    View-level permission to allow group-wise access to the view-based-apis.
    """
            
    def has_permission(self, request, view):  
        view = View.objects.get(view_name=view.__class__.__name__)
        user_groups = request.user.groups.all()
        if view.permission_groups.filter(name__in=list(user_groups)).exists():
            common_groups = view.permission_groups.filter(name__in=list(user_groups))
            logger.info("Permission granted for view: %s to user: %s of group: %s"%(view.view_name, request.user, common_groups))
            return True
        else:
            logger.info("Permission denied for view: %s to user: %s of groups: %s"%(view.view_name, request.user, user_groups))
            return False
