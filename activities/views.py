# default imports
from django.shortcuts import render

# model imports
from videos.models import *
from activities.models import *

# serializers imports
from activities.serializers import *

# drf imports
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

# authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

import logging
logger = logging.getLogger('coco_api')

class ScreeningAPIView( generics.ListCreateAPIView):
    ''' 
    coco_api class-based view to query Screening model and provide JSON response.
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
        logger.info("accessed: %s.ScreeningAPIView.post, user: %s" % ( __name__,user_obj))

        queryset = Screening.objects.get_queryset().order_by('id')

        uc_id = request.POST.get('user_created') # POST param 'user_created', default value is empty string
        if uc_id:
            queryset = queryset.filter(user_created__exact=uc_id) # filters for numeric values with exact match 

        start_day = request.POST.get('start_day')
        start_month = request.POST.get('start_month')
        start_year = request.POST.get('start_year')
        end_day = request.POST.get('end_day')
        end_month = request.POST.get('end_month')
        end_year = request.POST.get('end_year')

        # case1: all values are present
        if start_day and start_month and start_year and end_day and end_month and end_year:
            # params type value is string, trimmed spaces,convert to int and then make date by combining values
            try:
                start_date = datetime.date(int(start_year.strip()),int(start_month.strip()), int(start_day.strip()))
                end_date = datetime.date(int(end_year.strip()),int(end_month.strip()), int(end_day.strip()))       
                queryset = queryset.filter(date__range=(start_date, end_date)) # filters values in date range
            except:
                print("Date error occurred")
        # case2: only start values are present 
        elif start_day and start_month and start_year and not end_day and not end_month and not end_year:
            try:
                start_date = datetime.date(int(start_year.strip()),int(start_month.strip()), int(start_day.strip()))      
                queryset = queryset.filter(date__gte=start_date) # filters values greater than or equal to start date
            except:
                print("Start Date error occurred")
        # case3: only end values are present 
        elif not start_day and not start_month and not start_year and  end_day and  end_month and  end_year:
            try:
                end_date = datetime.date(int(end_year.strip()),int(end_month.strip()), int(end_day.strip()))       
                queryset = queryset.filter(date__lte=end_date) # filters values less than or equal to end date
            except:
                print("End Date error occurred")

        start_limit = request.POST.get('start_limit') # POST param 'start_limit'
        end_limit = request.POST.get('end_limit') # POST param 'end_limit'  

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

        fields_values = request.POST.get('fields', '') # POST param 'fields', default value is empty string
        if fields_values: # fields provided in POST request and if not empty serves those fields only
            fields_values = [val.strip() for val in fields_values.split(",")]
            # updated queryset is passed and fields provided in POST request is passed to the dynamic serializer
            serializer = ScreeningSerializer(queryset, fields=fields_values, many=True)
        else:
            # if fields param is empty then all the fields as mentioned in serializer are served to the response
            serializer = ScreeningSerializer(queryset, many=True)

        # context = RequestContext(request)
        # context_dict = {}
        # # Update the dictionary with csrf_token 
        # conext_dict.update(csrf(request))

        # JSON Response is provided by default
        return Response(serializer.data) #, context_dict, context)