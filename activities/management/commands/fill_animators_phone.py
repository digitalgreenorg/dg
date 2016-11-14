from django.core.management.base import BaseCommand
import os, sys
from os import path
import django
from django.db.models import Count
from django.db import IntegrityError
from activities.models import *
from people.models import *
from raw_data_analytics.utils.data_library import data_lib


class Command(BaseCommand):
    def handle(self,*args,**options):
    	animator_list = Animator.objects.filter(phone_no = '')
    	print "Animator Size before = "
    	animator_list = Animator.objects.filter(phone_no = '')
    	print animator_list.count()
    	print "Animator Data = "
    	phone_number_counter = 1
    	print type(animator_list)
    	for animator in animator_list :
    		animator.phone_no = phone_number_counter
    		animator.save()
    		phone_number_counter = phone_number_counter + 1

    	print "Animator Size = "
    	animator_list = Animator.objects.filter(phone_no = '')
    	print animator_list.count()
