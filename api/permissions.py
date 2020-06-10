from rest_framework import permissions
from api.models import View

# logger
import logging
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
