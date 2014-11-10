__author__ = 'Lokesh'
import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from geographies.models import District, Block
import pandas as pd
import MySQLdb
import pandas.io.sql as psql


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    make_option('-p', '--partner',
                    action='store',
                    default=False,
                    dest='partner',
                    help='Takes partner name as input'),
    make_option('-d', '--district',
                    action='store',
                    default=False,
                    dest='district',
                    help='Takes district name as input'),
    make_option('-b', '--block',
                    action='store',
                    default=False,
                    dest='block',
                    help='Takes block name as input'),
    )

    def handle(self, *args, **options):
        print args
        print options
        print "$$$$$$$$$$$$$$$$$$$"
        if(options['block']!=False):
            block = [options['block']]
            if(options['district']!=False):
                district = [options['district']]
        else:
            if(options['district']!=False):
                district = [options['district']]
                block = Block.objects.all(district__district_name=options['district']).values('id','block_name')
            else:
                if(options['partner']!=False):
                    partner = [options['partner']]

        self.home('RMNT','Khandwa','Khalwa')

    def home(self,partner_name,district_name,block_name):
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        df_mysql = psql.read_sql(
            (
            'select V.village_name, B.block_name, D.district_name, D.state_id, count(SC.id) from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id where P.partner_name=%s and D.district_name=%s and B.block_name=%s group by V.village_name'),
            con=mysql_cn, params=(partner_name, district_name, block_name))
#        print 'loaded dataframe from MySQL. records:', len(df_mysql)
#        print "################################"
#        print df_mysql
        mysql_cn.close()