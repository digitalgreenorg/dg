__author__ = 'Lokesh'
__author__ = 'Lokesh'
import json, datetime
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import pandas as pd
import MySQLdb
import pandas.io.sql as psql


class Command(BaseCommand):
    def handle(self, *args, **options):
        if(count(args)==3):

        self.home(a,b,c)

    def home(self,a,b,c):
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        df_mysql = psql.read_sql(
            (
            'select V.village_name, B.block_name, D.district_name, D.state_id, count(SC.id) from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id where P.partner_name=%s and D.district_name=%s and B.block_name=%s group by V.village_name'),
            con=mysql_cn, params=('RMNT', 'Khandwa', 'Khalwa'))
        print 'loaded dataframe from MySQL. records:', len(df_mysql)
        print "################################"
        print df_mysql
        mysql_cn.close()