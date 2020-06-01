# default imports
from django.shortcuts import render

# added imports
from rest_framework import viewsets, generics
from rest_framework import permissions, filters
from rest_framework.response import Response

# serializers import 
from people.serializers import FarmerSerializer

# model imports
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

from coco_api_utils import Utils

from django.contrib.auth.models import User

import logging
logger = logging.getLogger('coco_api')

class DefaultView(generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to provide default message in JSON format.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''
    
    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permissions_classes =[IsAuthenticated]

    # POST request
    def post(self, request, *args, **kwargs):
        # dictionary results as JSON format message 
        return Response({"message":"Welcome to COCO APIs", "base_url":"/farmer/api", 
        "url_list":["/farmer/api/farmers", "/farmer/api/csv"]})
    
    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed."})


class FarmersJsonAPIView(viewsets.GenericViewSet): #(generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to query Person model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permissions_classes =[IsAuthenticated]


    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def getAllFarmers(self, request, *args, **kwargs):
        user_obj = User.objects.get(username=request.user)
        logger.info("accessed: %s.getAllFarmers, user: %s" % ( __name__,user_obj))

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
        if phoneNumberExists in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'       

        utils = Utils()
        queryset = utils.limitQueryset(queryset=queryset, start_limit=start_limit, end_limit=end_limit) 

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data)

    # POST request
    def getPhoneMatchedResults(self, request, *args, **kwargs):
        user_obj = User.objects.get(username=request.user)
        logger.info("accessed: %s.getPhoneMatchedResults, user: %s" % ( __name__,user_obj))

        queryset = Person.objects.all().order_by('id')

        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        phone_numbers = request.POST.get('phoneNumbers', '') # POST param 'fields', default value is empty string

        phoneNumberExists = request.POST.get('phoneNumberExists','') # POST param 'filter_phone_no', default value is empty string

        # phone number exists or not    
        if phoneNumberExists in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])


        # phone number matches     
        if phone_numbers:
            ph_no_values = [ph.strip() for ph in phone_numbers.split(",")]
            queryset = queryset.filter(phone_no__in=ph_no_values)

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})


        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'      
        utils = Utils()
        queryset = utils.limitQueryset(queryset=queryset, start_limit=start_limit, end_limit=end_limit) 
  

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)
        # JSON Response is provided
        return Response(serializer.data)


class FarmersCsvAPIView(APIView):
    ''' 
    coco_api class-based view to query Person model and provide CSV response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''
    
    # CSV Renderer class setting to return response of this view as CSV
    renderer_classes = (r.CSVRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    
    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permissions_classes =[IsAuthenticated]

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request, *args, **kwargs):
        user_obj = User.objects.get(username=request.user)
        logger.info("accessed: %s.FarmersCsvAPIView.post, user: %s" % (__name__,user_obj))
        country_id = self.request.POST.get('country_id', 0) # POST param 'country_id', default value is 0
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        try:
            # fetches country id from database model Country to verify param value
            got_country_id = Country.objects.get(id=country_id).id 
            # if the country id is found same as param value entered, filters Person model  
            queryset = Person.objects.all().filter(village__block__district__state__country__exact=got_country_id).order_by('id')
        except:
            # in case of failure of above try statement, all Person objects are retrieved
            queryset = Person.objects.all().order_by('id')

        phoneNumberExists = request.POST.get('phoneNumberExists','') # POST param 'filter_phone_no', default value is empty string

        # phone number exists or not    
        if phoneNumberExists in ["true","t","yes","y"]:
            queryset = queryset.filter(phone_no__isnull=False).exclude(phone_no__in=[''])

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'       

        utils = Utils()
        queryset = utils.limitQueryset(queryset=queryset, start_limit=start_limit, end_limit=end_limit) 

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})
            
        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = FarmerSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = FarmerSerializer(queryset, many=True)
        # CSV Response is provided
        return Response(serializer.data)