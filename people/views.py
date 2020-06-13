# default imports
from django.shortcuts import render
# rest framework imports
from rest_framework import viewsets, generics
from rest_framework import permissions, filters
from rest_framework.response import Response
# app import 
from people.serializers import FarmerSerializer
from people.models import *
from geographies.models import *
# django-rest-framework TokenAuthentication imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# CSV View imports
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
# logging, pagination and permissions
import time
from api.utils import Utils, CustomPagination
from api.permissions import IsAllowed

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"      

class FarmerInfoView(generics.ListCreateAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to provide default message in JSON format.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''
    
    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]

    # POST request
    def post(self, request, *args, **kwargs):
        # dictionary results as JSON format message 
        return Response({"message":"Welcome to COCO APIs", "base_url":"/farmer/api", 
        "url_list":["/farmer/api/farmers", "/farmer/api/csv"]})
    
    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed."})


class FarmersJsonAPIView(viewsets.GenericViewSet): 
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Person model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = FarmerSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def getAllFarmers(self, request, *args, **kwargs):
        """
        This function can take following optional POST params to filter on Person obects:   
        1.) country_id - to find people belonging to a country
        2.) phoneNumberExists - to find people with valid phone numbers
        3.) fields - to pass comma separated value to be returned a value for each Person object, e.g. pass
                        fields value as id,person_name to get only these key-value pairs for each Person object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        country_id = self.request.POST.get('country_id', 0) # POST param 'country_id', default value is 0
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        phoneNumberExists = request.POST.get('phoneNumberExists','') # POST param 'filter_phone_no', default value is empty string

        try:
            # fetches country id from database model Country to verify param value
            got_country_id = Country.objects.get(id=country_id).id 
            # if the country id is found same as param value entered, filters Person model  
            queryset = Person.objects.all().filter(village__block__district__state__country__exact=got_country_id).order_by('id')
        except:
            # in case of failure of above try statement, all Person objects are retrieved
            queryset = Person.objects.all().order_by('id')

        # phone number exists or not 
        if phoneNumberExists.lower() in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])    

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
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response

    # POST request
    def getPhoneMatchedResults(self, request, *args, **kwargs):
        """
        This function can take following optional POST params to filter on Person obects:   
        1.) country_id - to find people belonging to a country
        2.) phoneNumberExists - to find people with valid phone numbers
        3.) phone_numbers - to pass comma separated value to search for exact phone numbers
        4.) fields - to pass comma separated value to be returned a value for each Person object, e.g. pass
                    fields value as id,person_name to get only these key-value pairs for each Person object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        queryset = Person.objects.all().order_by('id')

        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        phone_numbers = request.POST.get('phoneNumbers', '') # POST param 'fields', default value is empty string
        phoneNumberExists = request.POST.get('phoneNumberExists','') # POST param 'phoneNumberExists', default value is empty string

        # phone number exists or not    
        if phoneNumberExists.lower() in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])

        # phone number matches     
        if phone_numbers:
            ph_no_values = [ph.strip() for ph in phone_numbers.split(",")]
            queryset = queryset.filter(phone_no__in=ph_no_values)
    
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
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response


class FarmersCsvAPIView(viewsets.GenericViewSet):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Person model and provide CSV response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''
    
    # CSV Renderer class setting to return response of this view as CSV
    renderer_classes = (r.CSVRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    
    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    serializer_class = FarmerSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request, *args, **kwargs):
        """
        This function can take following optional POST params to filter on Person obects:   
        1.) country_id - to find people belonging to a country
        2.) phoneNumberExists - to find people with valid phone numbers
        3.) fields - to pass comma separated value to be returned a value for each Person object, e.g. pass
                    fields value as id,person_name to get only these key-value pairs for each Person object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        country_id = self.request.POST.get('country_id', 0) # POST param 'country_id', default value is 0
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        phoneNumberExists = request.POST.get('phoneNumberExists','') # POST param 'filter_phone_no', default value is empty string

        try:
            # fetches country id from database model Country to verify param value
            got_country_id = Country.objects.get(id=country_id).id 
            # if the country id is found same as param value entered, filters Person model  
            queryset = Person.objects.all().filter(village__block__district__state__country__exact=got_country_id).order_by('id')     
        except:
            # in case of failure of above try statement, all Person objects are retrieved
            queryset = Person.objects.all().order_by('id')

        # phone number exists or not    
        if phoneNumberExists.lower() in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])    

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response
