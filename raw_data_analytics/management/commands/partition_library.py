__author__ = 'Lokesh'
import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from geographies.models import District, Block
from configuration import tableDictionary, whereDictionary, selectDictionary, groupbyDictionary, categoryDictionary
import pandas as pd
import MySQLdb
import pandas.io.sql as psql
import xlsxwriter
import csv

class Command(BaseCommand):

    Dict={}
    lookup_matrix = {}
    # --- defining options for the command line exceution of the library ---
    option_list = BaseCommand.option_list + (
        make_option('-p', '--partner',
                    action='store',
                    default=False,
                    dest='partner',
                    help='Takes partner name as input for filter'),
        make_option('-c', '--country',
                    action='store',
                    default=False,
                    dest='country'
                         '',
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
        make_option('-a', '--animator',
                    action='store',
                    default=False,
                    dest='animator',
                    help='Takes mediator name as input for filter'),
        make_option('-w', '--numScreening',
                    action='store',
                    default=False,
                    dest='numScreening',
                    help='Takes nScreening as true or false to decide its inclusion in dataframe'),
        make_option('-u', '--numAdoption',
                    action='store',
                    default=False,
                    dest='numAdoption',
                    help='Takes nAdoption as true or false to decide its inclusion in dataframe'),
    )
    # --- options list for command line ends here ---

    # Function accepts the inputs and pass it to handle_controller for further processing
    def handle(self, *args, **options):
        fields_dict = {}
        fields_dict['partition'] = options['partition']
        print "%%%%%%%%%%%%%%%%%%%%%"
        print fields_dict['partition']
        fields_dict['value'] = options['value']
        print "###############"
        print fields_dict['value']

        self.lookup_matrix = self.read_lookup_csv()
        print self.lookup_matrix

        self.handle_controller(args, options, self.lookup_matrix)

    def handle_controller(self, args, options, lookup_matrix):
        # Accepts options i.e. dictionary of dictionary e.g. {'partition':{'partner':'','state',''},'value':{'nScreening':True,'nAdoption':true}}
        # This function is responsible to call function for checking validity of input and functions to make dataframes according to the inputs
        print "options is ---------"
        print options
        print "$$$$$$$$$$$$$$$$$$$"
        value_list_to_find = []
        relevantPartitionDictionary={}
        relevantValueDictionary={}

        # --- checking validity of the partition fields and value fields entered by user ---
        if self.check_partitionfield_validity(options['partition']):
            print "valid input for partition fields"
            for item in options['partition']:
                if options['partition'][item]!=False:
                    relevantPartitionDictionary[item] = options['partition'][item]
        else:
            print "Warning - Invalid input for partition fields"


        if self.check_valuefield_validity(options['value']):
            print "valid input for value fields"
            for item in options['value']:
                if options['value'][item]!=False:
                    relevantValueDictionary[item] = options['value'][item]
        else:
            print "Warning - Invalid input for Value fields"

        for input in relevantValueDictionary:
            queryComponents = self.getRequiredTables(relevantPartitionDictionary, input, lookup_matrix)
            print queryComponents
        return 0

    # Function to check validity of the partition field inputs by user by comparing with the generalPartitionList
    def check_partitionfield_validity(self, partitionField):
        print partitionField
        if set(partitionField.keys()).issubset(tableDictionary.keys()):
            return True
        else:
            return False

    # Function to check validity of the value field inputs by user by comparing with the generalValueList
    def check_valuefield_validity(self, valueField):
        if set(valueField.keys()).issubset(tableDictionary.keys()):
            return True
        else:
            return False

    def read_lookup_csv(self):
        file_data = csv.reader(open('C:/Users/Lokesh/Documents/dg/dg/media/raw_data_analytics/data_analytics.csv'))
        headers = next(file_data)
        headers.remove('')
        matrix = {}
        for row in file_data:
            sub_matrix = {}
            for i in range(0,len(headers)):
                sub_matrix[headers[i]]=[]
                temp = row[i+1].split('$')
                for t in temp:
                    sub_matrix[headers[i]].append(tuple(t.split('#')))
            matrix[row[0]] = sub_matrix

        for e in matrix:
            print '\n\n---'+str(e)+'::::'
            print str(matrix[e])
            print '\n\n'
        return matrix

    def getRequiredTables(self,partitionDict, valueDictElement, lookup_matrix):
        selectResult = self.getSelectComponent(partitionDict, valueDictElement)
        fromResult = self.getFromComponent(partitionDict,valueDictElement,lookup_matrix)
        whereResult = self.getWhereComponent(partitionDict, valueDictElement, self.Dict, lookup_matrix)
        groupbyResult = self.getGroupByComponent(partitionDict, valueDictElement)
        print "----------------------------------SELECT PART------------------------------"
        print selectResult
        print "----------------------------------FROM PART--------------------------------"
        print fromResult
        print "----------------------------------WHERE PART-------------------------------"
        print whereResult
        print "----------------------------------GROUP_BY PART----------------------------"
        print groupbyResult
        print "----------------------------------Full SQL Query---------------------------"
        query = self.makeSQLquery(selectResult,fromResult,whereResult,groupbyResult)
        print query
        print "-------------------------------Final Result--------------------------------"
        df = self.runQuery(query)
        print df
        print "---------------------------------Game Over---------------------------------"
        return '\n\nGetRequiredTables function got over where'


    def makeSQLquery(self,select_msg, from_msg, where_msg, groupby_msg):
        query = 'select '+str(select_msg)+' from '+str(from_msg)+' where '+str(where_msg)+' group by '+str(groupby_msg)
        return query

    def getSelectComponent(self,partitionElements,valueElement):
        selectComponentList = []
        for items in partitionElements:
            for i in selectDictionary[items]:
                if(selectDictionary[items][i]==True):
                    selectComponentList.append(tableDictionary[items] + '.' + i)
        print selectComponentList
        for i in selectDictionary[valueElement]:
            if(selectDictionary[valueElement][i]==True):
                selectComponentList.append(tableDictionary[valueElement] + '.' + i)

        print '??????????????????????\n????????????????????????????'
        print selectComponentList
        print '???????????????????????\n????????????????????????????'
        return ','.join(selectComponentList)

    def makeJoinTable(self,sourceTable,destinationTable,lookup_matrix,occuredTables,Dict):
        if(sourceTable not in occuredTables):
            for i in lookup_matrix[sourceTable][destinationTable]:
                if(i[2]=='self'):
                    print 'SELF'
                    return
                elif(i[2]=='direct'):
                    print 'DIRECT'
                    if(destinationTable not in occuredTables):
                        occuredTables.append(destinationTable)
                    if(destinationTable not in Dict[sourceTable]):
                        Dict[sourceTable].append(destinationTable)
                    occuredTables.append(sourceTable)
                    return
                else:
                    print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
                    print sourceTable
                    print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                    if(sourceTable in Dict.keys()):
                        Dict[sourceTable].append(i[2])
                    else:
                        Dict[sourceTable]=[i[2]]
                    occuredTables.append(sourceTable)
                    self.makeJoinTable(i[2],destinationTable,lookup_matrix,occuredTables,Dict)
        else:
            return

    def getFromComponent(self,partitionElements,valueElement,lookup_matrix):
        partitionTables = []
        for i in partitionElements:
            if(i in categoryDictionary['geographies']):
                partitionTables.insert(0,tableDictionary[i])
            else:
                partitionTables.append(tableDictionary[i])
        print '##############################################'
        print partitionTables
        print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        print tableDictionary[valueElement]
        print '*****************************************'

        majorTablesList = []
        tablesOccuredList = []
        for index, table in enumerate(partitionTables):
            minorTablePath=[]
            self.Dict[table]=[]
            if(table not in majorTablesList):
                minorTablePath.append(table)
                self.makeJoinTable(table,tableDictionary[valueElement],lookup_matrix,tablesOccuredList,self.Dict)
            print '()()()()()()()()()()()()()()()()()()()'
            print minorTablePath
            print 'Dict is -      - - - - ' + str(self.Dict)
            print '()()()()()()()()()()()()()()()()()()()'
        majorTablesList=tablesOccuredList
        print '!!!!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print majorTablesList
        print '!!!!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print 'testing From Component'
        return ' , '.join(majorTablesList)

    def getWhereComponent(self,partitionElements,valueElement, Dictionary, lookup_matrix):
        whereString = '1=1'
        whereComponentList = [whereString]
        for items in partitionElements:
            if partitionElements[items]!=True:
                whereComponentList.append(tableDictionary[items] + '.' + whereDictionary[items] + '=' + partitionElements[items])
        print '>>>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print whereComponentList
        print '>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        for i in Dictionary:
            for j in Dictionary[i]:
                whereComponentList.append(str(i)+'.'+str(lookup_matrix[i][j][0][0])+'='+str(j)+'.'+str(lookup_matrix[i][j][0][1]))
        return ' and '.join(whereComponentList)

    def getGroupByComponent(self,partitionElements,valueElement):
        groupbyComponentList = []
        for items in partitionElements:
            if partitionElements[items]==True:
                groupbyComponentList.append(tableDictionary[items]+'.'+groupbyDictionary[items])
        print '<<<<<<<<<<<<<<<<<<<<<<<<\n<<<<<<<<<<<<<<<<<<<<<<<<<<'
        print 'testing GroupBy Component'
        print '<<<<<<<<<<<<<<<<<<<<<<<\n<<<<<<<<<<<<<<<<<<<<<<<<<<<'
        return ' , '.join(groupbyComponentList)


    # Function to accept query as a string to execute and make dataframe corresponding to that particular query and return that dataframe

    def runQuery(self, query):
        # Make connection with the database
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        # Making dataframe
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df

    #
    #
    # def nScreeningDF(self, selectClause, whereClause, groupbyClause, sdate, edate):
    #     Screeningquery = 'select' + selectClause + ',count(SC.id) as nScreenings from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id join geographies_country C on S.country_id=C.id where' + whereClause + 'and SC.date between \'' + sdate + '\' and \'' + edate + '\'' + groupbyClause + ';'
    #     dfScreening = self.runQuery(Screeningquery)
    #     return dfScreening
    #
    # def nAdoptionDF(self, selectClause, whereClause, groupbyClause, sdate, edate):
    #     Adoptionquery = 'select' + selectClause + ',count(ADP.id) as nAdoptions from activities_personadoptpractice ADP join programs_partner P on P.id=ADP.partner_id join people_person PP on ADP.person_id=PP.id join geographies_village V on PP.village_id = V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id join geographies_country C on S.country_id=C.id where' + whereClause + 'and ADP.date_of_adoption between \'' + sdate + '\' and \'' + edate + '\'' + groupbyClause + ';'
    #     dfAdoption = self.runQuery(Adoptionquery)
    #     return dfAdoption
