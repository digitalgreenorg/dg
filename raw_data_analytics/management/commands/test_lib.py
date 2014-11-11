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
        whereClause = " 1=1 "
        groupbyClause = ' group by S.state_name'
        gflag = 0
        if(options['partner']!=False):
            whereClause += "and P.partner_name=\'"+options['partner']+"\'"
            groupbyClause = ' group by P.partner_name'
            gflag = 1
        if(options['district']!=False):
            whereClause += "and D.district_name=\'"+options['district']+"\'"
            if gflag==1:
                groupbyClause += ',B.block_name'
            else:
                groupbyClause = ' group by B.block_name'
        if(options['block']!=False):
            whereClause += "and B.block_name=\'"+options['block']+"\'"
            groupbyClause = ' group by V.village_name'
            if gflag == 1:
                groupbyClause += ',V.village_name'
            else:
                groupbyClause = ' group by V.village_name'

        self.home(whereClause,groupbyClause)

    def home(self,whereClause, groupbyClause):
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        df_mysql = psql.read_sql(
            ('select S.state_name, D.district_name, B.block_name, V.village_name, count(SC.id) as nScreenings from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id where'+whereClause+groupbyClause+';'),
            con=mysql_cn)
        print 'loaded dataframe from MySQL. records:', len(df_mysql)
        print "################################"
        print df_mysql

# 'select V.village_name, B.block_name, D.district_name, S.state_name, count(SC.id) from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_
# district D on B.district_id=D.id join geographies_state S on D.state_id=S.id where %s %s'
        mysql_cn.close()