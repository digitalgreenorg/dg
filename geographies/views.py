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

class DefaultView(viewsets.ViewSet):
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
    def post(self, request):
        # dictionary results as JSON format message 
        return Response({"message":"Welcome to COCO APIs", "base_url":"api/geo", 
        "url_list":["api/geo/village", 
                    "api/geo/block",
                    "api/geo/district",
                    "api/geo/state",
                    "api/geo/country"]})
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
    permissions_classes =[IsAuthenticated]

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request 
    def post(self, request, *args, **kwargs):

        queryset = Village.objects.get_queryset().order_by('id') # basic query to be filtered later in this method

        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)] 

        count = self.request.POST.get("count", "False")
        if count in ["True","true","t","T","Yes","yes","Y","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = VillageSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = VillageSerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data) 


class BlockAPIView(generics.ListAPIView):
    ''' 
    coco_api class-based view to query Block model and provide JSON response.
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
    def post(self, request, *args, **kwargs):
        
        queryset = Block.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value
        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]
        
        count = self.request.POST.get("count", "False")
        if count in ["True","true","t","T","Yes","yes","Y","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = BlockSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = BlockSerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data) 

class DistrictAPIView(generics.ListAPIView):
    ''' 
    coco_api class-based view to query District model and provide JSON response.
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
    def post(self, request, *args, **kwargs):
        
        queryset = District.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value
        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]

        count = self.request.POST.get("count", "False")
        if count in ["True","true","t","T","Yes","yes","Y","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = DistrictSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = DistrictSerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data) 

class StateAPIView(generics.ListAPIView):
    ''' 
    coco_api class-based view to query State model and provide JSON response.
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
    def post(self, request, *args, **kwargs):
        
        queryset = State.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value
        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]

        count = self.request.POST.get("count", "False")
        if count in ["True","true","t","T","Yes","yes","Y","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = StateSerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = StateSerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data)

class CountryAPIView(generics.ListAPIView):
    ''' 
    coco_api class-based view to query Country model and provide JSON response.
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
    def post(self, request, *args, **kwargs):
        
        queryset = Country.objects.get_queryset().order_by('id') # basic query to be filtered later in this method
        
        fields_values = request.POST.get('fields', '') # POST param 'limit', no default value specified so empty string is default value
        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

        # limits the total response count        
        if start_limit and end_limit: # case1: both are present
            queryset = queryset[int(start_limit)-1:int(end_limit)]
        elif start_limit: # case2: only start_limit is present
            queryset = queryset[int(start_limit)-1:]
        elif end_limit: # case3: only end_limit is present
            queryset = queryset[:int(end_limit)]

        count = self.request.POST.get("count", "False")
        if count in ["True","true","t","T","Yes","yes","Y","y"]:
            return Response({"count": queryset.count()})
            
        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = CountrySerializer(queryset, fields=fields_values ,many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = CountrySerializer(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data)