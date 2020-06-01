# default imports
from django.shortcuts import render

# rest_framework imports
from rest_framework import generics
from rest_framework.response import Response

# app imports
from models import *
from serializers import *

# authentication imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

import logging
logger = logging.getLogger('coco_api')

class PartnerAPIView(generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to query Partner model and provide JSON response.
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
        user_obj = User.objects.get(username=request.user)
        logger.info("accessed: %s.PartnerAPIView.post, user: %s" % ( __name__,user_obj))

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'
        fields_values = request.POST.get('fields', '') # POST param 'fields'
        partner_id = self.request.POST.get('id', 0) # POST param 'id'
        
        queryset = Partner.objects.all().order_by('id')
        serializer_class = PartnerSerializer

        if partner_id: # checks if video id is present
            queryset = queryset.filter(id__exact=partner_id)
        else:
            # limits the total response count        
            if start_limit and end_limit: # case1: both are present
                queryset = queryset[int(start_limit)-1:int(end_limit)]
            elif start_limit: # case2: only start_limit is present
                queryset = queryset[int(start_limit)-1:]
            elif end_limit: # case3: only end_limit is present
                queryset = queryset[:int(end_limit)]

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = serializer_class(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = serializer_class(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data)




class ProjectAPIView(generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to query Project model and provide JSON response.
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
        user_obj = User.objects.get(username=request.user)
        logger.info("accessed: %s.ProjectAPIView.post, user: %s" % ( __name__,user_obj))

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'
        fields_values = request.POST.get('fields', '') # POST param 'fields'
        project_id = self.request.POST.get('id', 0) # POST param 'id'
        
        queryset = Project.objects.all().order_by('id')
        serializer_class = ProjectSerializer

        if project_id: # checks if video id is present
            queryset = queryset.filter(id__exact=project_id)
        else:
            # limits the total response count        
            if start_limit and end_limit: # case1: both are present
                queryset = queryset[int(start_limit)-1:int(end_limit)]
            elif start_limit: # case2: only start_limit is present
                queryset = queryset[int(start_limit)-1:]
            elif end_limit: # case3: only end_limit is present
                queryset = queryset[:int(end_limit)]

        count = self.request.POST.get("count", "False") # POST param 'count', default value is string "False"
        # returns count only if param value matched
        if count.lower() in ["true","t","yes","y"]:
            return Response({"count": queryset.count()})

        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = serializer_class(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = serializer_class(queryset, many=True)
        # JSON Response is provided by default
        return Response(serializer.data)
