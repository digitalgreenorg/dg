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

    tablesDictionary = {'partner':('programs_partner','P'),'country':('geographies_country','C'),'state':('geographies_state','S'),'district':('geographies_district','D'),'block':('geographies_block','B'),'village':('geographies_village','V')}

    generalPartitionList = {'partner':False, 'country':False, 'state':False, 'district':False, 'block':False, 'village':False}
    generalValueList = {'nScreening':False, 'nAdoption':False}

    option_list = BaseCommand.option_list + (
    make_option('-p', '--partner',
                    action='store',
                    default=False,
                    dest='partner',
                    help='Takes partner name as input for filter'),
    make_option('-c', '--country',
                    action='store',
                    default=False,
                    dest='country',
                    help='Takes country name as input for filter'),
    make_option('-s', '--state',
                    action='store',
                    default=False,
                    dest='state',
                    help='Takes state name as input for filter'),
    make_option('-d', '--district',
                    action='store',
                    default=False,
                    dest='district',
                    help='Takes district name as input for filter'),
    make_option('-b', '--block',
                    action='store',
                    default=False,
                    dest='block',
                    help='Takes block name as input for filter'),
    make_option('-g', '--village',
                    action='store',
                    default=False,
                    dest='village',
                    help='Takes village name as input for filter'),
    make_option('-w', '--nScreening',
                    action='store',
                    default=False,
                    dest='nScreening',
                    help='Takes nScreening as true or false to decide its inclusion in dataframe'),
    make_option('-u', '--nAdoption',
                    action='store',
                    default=False,
                    dest='nAdoption',
                    help='Takes nAdoption as true or false to decide its inclusion in dataframe'),
    )

    def handle(self, *args, **options):
        temp1 = options
        temp2 = {}
        fields_dict = {}
        temp2['nScreening'] = temp1['nScreening']
        temp2['nAdoption'] = temp1['nAdoption']
        print "%%%%%%%%%%%%%%%%%%%%%"
        print temp2
        del temp1['nScreening']
        del temp1['nAdoption']
        del temp1['settings']
        del temp1['pythonpath']
        del temp1['verbosity']
        del temp1['traceback']
        print "###############"
        print temp1
        fields_dict['partition'] = temp1
        fields_dict['value'] = temp2

        self.handle_controller(fields_dict)


    def handle_controller(self, options):
        print "args is -------"
        print
        print "options is ---------"
        print options
        print "$$$$$$$$$$$$$$$$$$$"

        if self.check_partitionfield_validity(options['partition']):
            queryComponents = self.make_query_components(options['partition'])
            if self.check_valuefield_validity(options['value']):
                self.home(queryComponents[0], queryComponents[1], queryComponents[2])
            else:
                print "Check the value field inputs again"
        else:
            print "Check the partition field inputs again"



    def home(self, selectClause, whereClause, groupbyClause):

        # Make query to extract data and create dataframe for further processing
        Screeningquery = 'select'+ selectClause + ',count(SC.id) as nScreenings from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id join geographies_country C on S.country_id=C.id where' + whereClause + groupbyClause + ';'
        Adoptionquery = 'select' + selectClause + ',count(ADP.id) as nAdoptions from activities_personadoptpractice ADP join programs_partner P on P.id=ADP.partner_id join people_person PP on ADP.person_id=PP.id join geographies_village V on PP.village_id = V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id join geographies_country C on S.country_id=C.id where' + whereClause + groupbyClause + ';'

        df_mysql_screening = self.runQuery(Screeningquery)
        df_mysql_adoption = self.runQuery(Adoptionquery)

        df_mysql = pd.merge(df_mysql_screening,df_mysql_adoption, how='outer')
        print 'loaded dataframe from MySQL. records:', len(df_mysql)
        print Screeningquery
        print "################################"
        print Adoptionquery
        print df_mysql

    def runQuery(self, query):
        # Make connection with the database
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df

    def check_partitionfield_validity(self, partitionField):
        print "hurrrr"
        print partitionField
        if set(partitionField.keys()).issubset(self.generalPartitionList.keys()):
            print "Vella"
            return True
        else:
            print "Delha"
            return False

    def check_valuefield_validity(self, valueField):
        if set(valueField.keys()).issubset(self.generalValueList.keys()):
            return True
        else:
            return False

    def make_query_components(self, options):
        """ Add similar IF block for any new partition field and to add in groupbyClause, selectClause and whereClause """

        print "hello ji"
        print options
        gflag = 0
        sflag = 0
        groupbyClause = ''
        whereClause = " 1=1 "
        selectClause = ''

        # If section to check if user has selected partner for partition field/filter field
        if(options['partner']!=False):
            if gflag == 1:
                groupbyClause += ',' + self.tablesDictionary['partner'][1] + '.partner_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['partner'][1] + '.partner_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['partner'][1] + '.partner_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['partner'][1] + '.partner_name'

            if (options['partner']!='null'):
                whereClause += "and " + self.tablesDictionary['partner'][1] + ".partner_name=\'"+options['partner']+"\'"

        # If section to check if user has selected country for partition field/filter field
        if(options['country']!=False):
            if gflag == 1:
                groupbyClause += ',' + self.tablesDictionary['country'][1] + '.country_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['country'][1] + '.country_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['country'][1] + '.country_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['country'][1] + '.country_name'

            if (options['country']!='null'):
                whereClause += "and " + self.tablesDictionary['country'][1] + ".country_name=\'"+options['country']+"\'"

        # If section to check if user has selected state for partition field/filter field
        if(options['state']!=False):
            if gflag == 1:
                groupbyClause += ',' + self.tablesDictionary['state'][1] + '.state_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['state'][1] + '.state_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['state'][1] + '.state_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['state'][1] + '.state_name'

            if (options['state']!='null'):
                whereClause += "and " + self.tablesDictionary['state'][1] + ".state_name=\'"+options['state']+"\'"

        # If section to check if user has selected district for partition field/filter field
        if(options['district']!=False):
            if gflag==1:
                groupbyClause += ',' + self.tablesDictionary['district'][1] + '.district_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['district'][1] + '.district_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['district'][1] + '.district_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['district'][1] + '.district_name'

            if (options['district']!='null'):
                whereClause += "and " + self.tablesDictionary['district'][1] + ".district_name=\'"+options['district']+"\'"

        # If section to check if user has selected block for partition field/filter field
        if(options['block']!=False):
            if gflag == 1:
                groupbyClause += ',' + self.tablesDictionary['block'][1] + '.block_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['block'][1] + '.block_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['block'][1] + '.block_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['block'][1] + '.block_name'

            if (options['block']!='null'):
                whereClause += "and " + self.tablesDictionary['block'][1] + ".block_name=\'"+options['block']+"\'"

        # If section to check if user has selected village for partition field/filter field
        if(options['village']!=False):
            if gflag == 1:
                groupbyClause += ',' + self.tablesDictionary['village'][1] + '.village_name'
            else:
                gflag = 1
                groupbyClause = ' group by ' + self.tablesDictionary['village'][1] + '.village_name'
            if sflag == 1:
                selectClause += ',' + self.tablesDictionary['village'][1] + '.village_name '
            else:
                sflag = 1
                selectClause = ' ' + self.tablesDictionary['village'][1] + '.village_name'

            if (options['village']!='null'):
                whereClause += "and " + self.tablesDictionary['village'][1] + ".village_name=\'"+options['village']+"\'"

        return [selectClause, whereClause, groupbyClause]