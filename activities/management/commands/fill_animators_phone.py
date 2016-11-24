from django.core.management.base import BaseCommand
import os, sys
from os import path
import django
from django.db.models import Count
from django.db import IntegrityError
from activities.models import *
from people.models import *
from raw_data_analytics.utils.data_library import data_lib
from django.db.models import Q

class Command(BaseCommand):
    def handle(self,*args,**options):
    	animator_list = Animator.objects.filter(Q(phone_no = '')|Q(phone_no='0'))
    	print "Animator Size before = "
    	print animator_list.count()
    	phone_number_counter = 1
    	for animator in animator_list :
    		animator.phone_no = phone_number_counter
    		animator.save()
    		phone_number_counter = phone_number_counter + 1

    	print "Animator Size = "
    	animator_list = Animator.objects.filter(phone_no = '')
    	print animator_list.count()
