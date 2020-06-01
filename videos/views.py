#default
from django.shortcuts import render

# model imports
from videos.models import *

# serializers imports
from videos.serializers import *

# drf imports
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response

# django-rest-framework TokenAuthentication imports
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from coco_api_utils import Utils, CustomPagination
import time

class VideoAPIView(generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to query Videos model and provide JSON response.
    django-rest-framework based token passed in Header as {'Authorization': 'Token 12345exampleToken'} 
    is required to access data from this View.
    Only POST method is allowed.
    GET request sent will show a message : "Method \"GET\" not allowed."    
    '''

    # django-rest-framework TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permissions_classes =[IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = VideoSerializer

    # GET request 
    def get(self, request):
        return Response({"detail":"Method \"GET\" not allowed"})

    # POST request
    def post(self, request, *args, **kwargs):
        start_time = time.time()
        utils = Utils()

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'
        fields_values = request.POST.get('fields', '') # POST param 'fields'
        video_id = self.request.POST.get('id', 0) # POST param 'id'
        
        if video_id: # checks if video id is present
            queryset = Video.objects.filter(id__exact=video_id)
        else:
            queryset = Video.objects.all().order_by('id')
            # limits the total response count        
            queryset = utils.limitQueryset(queryset=queryset, start_limit=start_limit, end_limit=end_limit) 

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = VideoSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = VideoSerializer(queryset, many=True)
        
        response = Response(serializer.data)


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data) 
            processing_time = time.time() - start_time
            utils.logRequest(request, self, self.post.__name__ , processing_time, paginated_response.status_code)
            return paginated_response

        processing_time = time.time() - start_time
        utils.logRequest(request, self, self.post.__name__ , processing_time, response.status_code)
        # JSON Response is provided
        return response
  
