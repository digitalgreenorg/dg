import urllib2
import unicodecsv as csv
import xml.etree.ElementTree as ET
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from qacoco.models import *
from geographies.models import *
from programs.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        #5,6,15 denoted Bihar,A.P. and Telangana
        block_list = Block.objects.filter(district__state_id__in = (5,6,15))
        partner_obj = {}
        partner_obj[5] = Partner.objects.get(id=11)
        partner_obj[6] = Partner.objects.get(id=9)
        partner_obj[15] = Partner.objects.get(id=9)
        regex = re.compile('[^a-zA-Z0-9]')
        names = ""
        not_created = ""
        for block in block_list:
            district_name = block.district.district_name
            block_name = block.block_name
            district_name = regex.sub('',district_name).lower()
            block_name = regex.sub('',block_name).lower()
            if district_name == '' or block_name == '':
                continue
            username = 'dg_' + str(district_name) + '_' + str(block_name) 
            if len(username) > 30:
                not_created += username + '\n'
                continue
            exist = User.objects.filter(username=username).count()
            user_obj = ''
            if exist <= 0:
                user_obj = User.objects.create_user(username, password=username)
                user_obj.save()
            else:
                user_obj = User.objects.get(username=username)
                if QACocoUser.objects.filter(user=user_obj).count() > 0:
                    print username
                    continue
            qacoco_user_obj = QACocoUser(user=user_obj,partner=partner_obj[block.district.state.id])
            qacoco_user_obj.save()
            qacoco_user_obj.blocks.add(block)
            names += username + '\n'
            
        with open('qacoco_usernames','w+') as test:
            test.write(names)

        with open('qacoco_notcreated_usernames','w+') as test:
            test.write(not_created)
