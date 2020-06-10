#default imports
from django.shortcuts import render

# added imports
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# serializers import 
from geographies.serializers import *

# model imports
from geographies.models import *

# django-rest-framework TokenAuthentication imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# logging, pagination and permissions
import time
from api.utils import Utils, CustomPagination
from api.permissions import IsAllowed

class DefaultView(generics.ListAPIView):
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
    permission_classes =[IsAuthenticated and IsAllowed]

    # POST request
    def post(self, request):
        # dictionary results as JSON format message 
        return Response({"message":"Welcome to COCO APIs", "base_url":"/geo/api/", 
        "url_list":["/geo/api/village", 
                    "/geo/api/block",
                    "/geo/api/district",
                    "/geo/api/state",
                    "/geo/api/country"]})
    # GET request
    def get(self, request, *args, **kwargs):
        return Response({"detail":"Method \"GET\" not allowed"})
          
        
class VillageAPIView(generics.ListAPIView):
    ''' 
    coco_api class-based view to query Village model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication  
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = VillageSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        queryset = Village.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = VillageSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = VillageSerializer(queryset, many=True)
        
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


class BlockAPIView(generics.ListAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Block model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication  
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = BlockSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        queryset = Block.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = BlockSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = BlockSerializer(queryset, many=True)

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

class DistrictAPIView(generics.ListAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query District model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication  
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = DistrictSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        queryset = District.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = DistrictSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = DistrictSerializer(queryset, many=True)

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

class StateAPIView(generics.ListAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query State model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = StateSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        queryset = State.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = StateSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = StateSerializer(queryset, many=True)

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

class CountryAPIView(generics.ListAPIView):
    ''' 
    This view is specifically written for coco api access.
    This class-based view is to query Country model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated and IsAllowed]
    pagination_class = CustomPagination
    serializer_class = CountrySerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        queryset = Country.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value
            
        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = CountrySerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = CountrySerializer(queryset, many=True)

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