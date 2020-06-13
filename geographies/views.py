# django imports
from django.shortcuts import render
# rest framework imports
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# rest framework TokenAuthentication imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# pagination and permissions
import time
from api.utils import Utils, CustomPagination
from api.permissions import IsAllowed
# app imports 
from geographies.serializers import *
from geographies.models import *

__author__ = "Stuti Verma"
__credits__ = ["Sujit Chaurasia", "Sagar Singh"]
__email__ = "stuti@digitalgreen.org"
__status__ = "Development"      

class GeoInfoView(generics.ListAPIView):
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

    # GET request
    def get(self, request, *args, **kwargs):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request):
        # dictionary results as JSON format message 
        return Response({"message":"Welcome to COCO APIs", "base_url":"/geo/api/", 
        "url_list":["/geo/api/village", 
                    "/geo/api/block",
                    "/geo/api/district",
                    "/geo/api/state",
                    "/geo/api/country"]})
        
        
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
        """
        This function can take following optional POST params to filter on Village obects:   
        1.) id - to find village by id
        2.) fields - to pass comma separated value to be returned a value for each Village object, e.g. pass
        fields value as id,village_name to get only these key-value pairs for each Village object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        village_id = self.request.POST.get('id', 0) # POST param 'id'
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if village_id: 
            queryset = Village.objects.filter(id__exact=village_id) # to search by id
        else:
            queryset = Village.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
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
            serializer = VillageSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = VillageSerializer(queryset, many=True)

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
        """
        This function can take following optional POST params to filter on Block obects:   
        1.) id - to find block by id
        2.) fields - to pass comma separated value to be returned a value for each Block object, e.g. pass
        fields value as id,block_name to get only these key-value pairs for each Block object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        block_id = self.request.POST.get('id', 0) # POST param 'id'
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if block_id: 
            queryset = Block.objects.filter(id__exact=block_id) # to search by id
        else:
            queryset = Block.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

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
            serializer = BlockSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = BlockSerializer(queryset, many=True)
        
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
        """
        This function can take following optional POST params to filter on District obects:   
        1.) id - to find district by id
        2.) fields - to pass comma separated value to be returned a value for each District object, e.g. pass
        fields value as id,district_name to get only these key-value pairs for each District object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        district_id = self.request.POST.get('id', 0) # POST param 'id'
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if district_id: 
            queryset = District.objects.filter(id__exact=district_id) # to search by id
        else:
            queryset = District.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

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
            serializer = DistrictSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = DistrictSerializer(queryset, many=True)

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
        """
        This function can take following optional POST params to filter on State obects:   
        1.) id - to find state by id
        2.) fields - to pass comma separated value to be returned a value for each State object, e.g. pass
        fields value as id,state_name to get only these key-value pairs for each State object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        state_id = self.request.POST.get('id', 0) # POST param 'id'
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if state_id: 
            queryset = State.objects.filter(id__exact=state_id) # to search by id
        else:
            queryset = State.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

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
            serializer = StateSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = StateSerializer(queryset, many=True)

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
        """
        This function can take following optional POST params to filter on Country obects:   
        1.) id - to find country by id
        2.) fields - to pass comma separated value to be returned a value for each Country object, e.g. pass
        fields value as id,country_name to get only these key-value pairs for each Country object

        If none of the above parameters are provided, then all the objects from respective model
        will be sent to the response.
        """

        start_time = time.time()
        utils = Utils()

        country_id = self.request.POST.get('id', 0) # POST param 'id'
        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string

        if country_id: 
            queryset = Country.objects.filter(id__exact=country_id) # to search by id
        else:
            queryset = Country.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

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
            serializer = CountrySerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = CountrySerializer(queryset, many=True)

        response = Response(serializer.data)
        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response
