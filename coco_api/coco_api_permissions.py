from rest_framework import permissions
from constants import PERMISSIONS_MAP


import logging
logger = logging
logger = logging.getLogger('coco_api')


class IsDGRestricted(permissions.BasePermission):
    """
    View-level permission to allow restricted access to the view-based-apis.
    Assumes the group of external partners exists who can't access it.
    """

    def has_permission(self, request, view):  
        view_name = view.__class__.__name__
        if PERMISSIONS_MAP.has_key(view_name):
            for group_name in PERMISSIONS_MAP.get(view_name):
                if  request.user.groups.filter(name=group_name).exists():
                    logger.info("Permission granted for view: %s to user: %s of group: %s"%(view_name, request.user, group_name))
                    return True
        else:
            logger.info("Permission denied for view: %s to user: %s"%(view_name, request.user))
            return False