"""
This file consists of views for activities.models
"""
# default imports
from django.shortcuts import render
# rest framework imports
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# app imports
from videos.models import *
from activities.models import *
from activities.serializers import *
# authentication imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# logging, pagination and permission imports
import time
from api.utils import Utils, CustomPagination
from api.permissions import IsAllowed

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"

class ScreeningAPIView( generics.ListCreateAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Screening model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = ScreeningSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request, *args, **kwargs):
        """
        This function can take following optional POST params to filter on Screening obects: 
        user_created_id -  this is id associated with CoCoModel inherited by Screening model, 
        start_day - takes day part value of a search in date range, 
        start_month - takes month part value of a search in date range, 
        start_year - takes year part value of a search in date range, 
        end_day - takes day part value of a search in date range, 
        end_month - takes month part value of a search in date range, 
        end_year - takes year part value of a search in date range,  
        fields - to pass comma separated value to be returned a value for each Screening object, e.g. pass
        fields value as id,user_created to get only these key-value pairs for each Screening object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()
        
        queryset = Screening.objects.get_queryset().order_by('id')
        
        start_day = request.POST.get('start_day')
        start_month = request.POST.get('start_month')
        start_year = request.POST.get('start_year')
        end_day = request.POST.get('end_day')
        end_month = request.POST.get('end_month')
        end_year = request.POST.get('end_year')
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        uc_id = request.POST.get('user_created_id') # POST param 'user_created', default value is empty string

        if uc_id:
            queryset = queryset.filter(user_created__exact=uc_id) # filters for numeric values with exact match 

        # case1: all values are present
        if start_day and start_month and start_year and end_day and end_month and end_year:
            # params type value is string, trimmed spaces,convert to int and then make date by combining values
            try:
                start_date = datetime.date(int(start_year.strip()), int(start_month.strip()), int(start_day.strip()))
                end_date = datetime.date(int(end_year.strip()), int(end_month.strip()), int(end_day.strip()))       
                queryset = queryset.filter(date__range=(start_date, end_date)) # filters values in date range
            except:
                utils.logMessage(self, self.post.__name__, "Date error occurred")
        # case2: only start values are present 
        elif start_day and start_month and start_year and not end_day and not end_month and not end_year:
            try:
                start_date = datetime.date(int(start_year.strip()), int(start_month.strip()), int(start_day.strip()))      
                queryset = queryset.filter(date__gte=start_date) # filters values greater than or equal to start date
            except:
                utils.logMessage(self, self.post.__name__, "Start Date error occurred")
        # case3: only end values are present 
        elif not start_day and not start_month and not start_year and end_day and end_month and end_year:
            try:
                end_date = datetime.date(int(end_year.strip()), int(end_month.strip()), int(end_day.strip()))       
                queryset = queryset.filter(date__lte=end_date) # filters values less than or equal to end date
            except:
                utils.logMessage(self, self.post.__name__, "End Date error occurred")

        page = self.paginate_queryset(queryset)
        if page is not None:
            if fields_values: # fields provided in POST request and if not empty serves those fields only
                fields_values = [val.strip() for val in fields_values.split(",")]
                # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
                serializer = self.get_serializer(page, fields=fields_values, many=True)
            else:
                # if fields param is empty then all the fields as mentioned in serializer are served to the response
                serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data) 
            processing_time = time.time() - start_time
            utils.logRequest(request, self, self.post.__name__ , processing_time, paginated_response.status_code)
            return paginated_response
        
        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = ScreeningSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = ScreeningSerializer(queryset, many=True)

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response