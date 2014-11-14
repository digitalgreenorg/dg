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
    make_option('-s', '--state',
                    action='store',
                    default=False,
                    dest='state',
                    help='Takes state name as input'),
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
        sflag = 0
        selectClause = ''

        if(options['partner']!=False):
            if gflag == 1:
                groupbyClause += ',P.partner_name'
            else:
                gflag = 1
                groupbyClause = ' group by P.partner_name'
            if sflag == 1:
                selectClause += ',P.partner_name '
            else:
                sflag = 1
                selectClause = ' P.partner_name'

            if (options['partner']!='null'):
                whereClause += "and P.partner_name=\'"+options['partner']+"\'"

        if(options['state']!=False):
            if gflag == 1:
                groupbyClause += ',S.state_name'
            else:
                gflag = 1
                groupbyClause = ' group by S.state_name'
            if sflag == 1:
                selectClause += ',S.state_name '
            else:
                sflag = 1
                selectClause = ' S.state_name'

            if (options['state']!='null'):
                whereClause += "and S.state_name=\'"+options['state']+"\'"

        if(options['district']!=False):
            if gflag==1:
                groupbyClause += ',D.district_name'
            else:
                gflag = 1
                groupbyClause = ' group by D.district_name'
            if sflag == 1:
                selectClause += ',D.district_name '
            else:
                sflag = 1
                selectClause = ' D.district_name'

            if (options['district']!='null'):
                whereClause += "and D.district_name=\'"+options['district']+"\'"

        if(options['block']!=False):
            if gflag == 1:
                groupbyClause += ',B.block_name'
            else:
                gflag = 1
                groupbyClause = ' group by B.block_name'
            if sflag == 1:
                selectClause += ',B.block_name '
            else:
                sflag = 1
                selectClause = ' B.block_name'

            if (options['block']!='null'):
                whereClause += "and B.block_name=\'"+options['block']+"\'"

        self.home(selectClause, whereClause, groupbyClause)

    def home(self, selectClause, whereClause, groupbyClause):
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        query = 'select'+ selectClause + ',count(SC.id) as nScreenings from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id where'+whereClause+groupbyClause+';'
        df_mysql = psql.read_sql(query,con=mysql_cn)
        print 'loaded dataframe from MySQL. records:', len(df_mysql)
        print query
        print "################################"
        print df_mysql
        mysql_cn.close()