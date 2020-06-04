from django.contrib.auth.models import User
from django.utils import importlib

import time
import logging

# pagination
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class Utils:

    def limitQueryset(self, queryset, start_limit, end_limit):
        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]

        return queryset



    def logRequest(self, request, class_instance, view_fun, processing_time, status_code ):
        logger = logging.getLogger('coco_api')
        user_obj = User.objects.get(username=request.user)
        ip_addr = request.META['REMOTE_ADDR']
        method = request.method
        user_id = user_obj.id
        class_name = class_instance.__class__.__name__
        module_name = class_instance.__module__
        # method_name = fun.
        logger.info("Accessed: %s.%s.%s, user_id: %s, username: %s, ip_address: %s, method: %s, processing_time: %s seconds, status_code: %s" % ( module_name, class_name, view_fun, user_id, user_obj, ip_addr, method, processing_time, status_code))