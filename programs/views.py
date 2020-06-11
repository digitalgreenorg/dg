# default imports
from django.shortcuts import render
# rest_framework imports
from rest_framework import generics, viewsets
from rest_framework.response import Response
# app imports
from programs.models import *
from programs.serializers import *
# authentication imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# logging, pagination and permissions
import time
from api.utils import Utils, CustomPagination
from api.permissions import IsAllowed


class PartnerAPIView(generics.ListCreateAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Partner model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = PartnerSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def getPartnerById(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        # start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        # end_limit = request.POST.get('end_limit') # POST param 'end_limit'
        fields_values = request.POST.get('fields', '') # POST param 'fields'
        partner_id = self.request.POST.get('id', 0) # POST param 'id'
        
        queryset = Partner.objects.all().order_by('id')
        serializer_class = PartnerSerializer

        if partner_id: # checks if video id is present
            queryset = queryset.filter(id__exact=partner_id)

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = serializer_class(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            if fields_values: # fields provided in POST request and if not empty serves those fields only
                # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
                serializer = self.get_serializer(page, fields=fields_values, many=True)
            else:
                # if fields param is empty then all the fields as mentioned in serializer are served to the response
                serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data) 
            processing_time = time.time() - start_time
            utils.logRequest(request, self, self.post.__name__ , processing_time, paginated_response.status_code)
            return paginated_response

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response


class ProjectAPIView(generics.ListCreateAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Project model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = ProjectSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        fields_values = request.POST.get('fields', '') # POST param 'fields'
        project_id = self.request.POST.get('id', 0) # POST param 'id'
        
        queryset = Project.objects.all().order_by('id')
        serializer_class = ProjectSerializer

        if project_id: # checks if video id is present
            queryset = queryset.filter(id__exact=project_id)

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = serializer_class(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            if fields_values: # fields provided in POST request and if not empty serves those fields only
                # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
                serializer = self.get_serializer(page, fields=fields_values, many=True)
            else:
                # if fields param is empty then all the fields as mentioned in serializer are served to the response
                serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data) 
            processing_time = time.time() - start_time
            utils.logRequest(request, self, self.post.__name__ , processing_time, paginated_response.status_code)
            return paginated_response

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response

        