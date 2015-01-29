__author__ = 'Lokesh'
import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from configuration import tableDictionary, whereDictionary, selectDictionary, groupbyDictionary, categoryDictionary
import pandas as pd
import MySQLdb
import pandas.io.sql as psql
import csv


class Command(BaseCommand):
    Dict = {}
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
        self.lookup_matrix = self.read_lookup_csv()
        result_dataframe = self.handle_controller(args, options, self.lookup_matrix)
        print "--------------FINAL RESULT---------------"
        print result_dataframe
        

    def handle_controller(self, args, options, lookup_matrix):
        # Accepts options i.e. dictionary of dictionary e.g. {'partition':{'partner':'','state',''},'value':{'nScreening':True,'nAdoption':true}}
        # This function is responsible to call function for checking validity of input and functions to make dataframes according to the inputs

        relevantPartitionDictionary = {}
        relevantValueDictionary = {}
        # --- checking validity of the partition fields and value fields entered by user ---
        if self.check_partitionfield_validity(options['partition']):
            print "valid input for partition fields"
            for item in options['partition']:
                if options['partition'][item] != False:
                    relevantPartitionDictionary[item] = options['partition'][item]
        else:
            print "Warning - Invalid input for partition fields"

        if self.check_valuefield_validity(options['value']):
            print "valid input for value fields"
            for item in options['value']:
                if options['value'][item] != False:
                    relevantValueDictionary[item] = options['value'][item]
        else:
            print "Warning - Invalid input for Value fields"


        final_df = pd.DataFrame()

        for input in relevantValueDictionary:
            queryComponents = self.getRequiredTables(relevantPartitionDictionary, input, args, lookup_matrix)
            print queryComponents
            print "----------------------------------Full SQL Query---------------------------"
            query = self.makeSQLquery(queryComponents[0],queryComponents[1],queryComponents[2],queryComponents[3])
            print query
            print "-------------------------------Final Result--------------------------------"
            df = self.runQuery(query)
            if final_df.empty:
                final_df = df
            else:
                final_df = pd.merge(final_df, df, how='outer')
            print df
            print "---------------------------------Game Over---------------------------------"
        return final_df

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
            for i in range(0, len(headers)):
                sub_matrix[headers[i]] = []
                temp = row[i + 1].split('$')
                for t in temp:
                    sub_matrix[headers[i]].append(tuple(t.split('#')))
            matrix[row[0]] = sub_matrix
        return matrix

    def getRequiredTables(self, partitionDict, valueDictElement, args, lookup_matrix):
        self.Dict.clear()
        selectResult = self.getSelectComponent(partitionDict, valueDictElement)
        fromResult = self.getFromComponent(partitionDict, valueDictElement, lookup_matrix)
        whereResult = self.getWhereComponent(partitionDict, valueDictElement, self.Dict, lookup_matrix)
        groupbyResult = self.getGroupByComponent(partitionDict, valueDictElement)
        print "----------------------------------SELECT PART------------------------------"
        print selectResult
        print "----------------------------------FROM PART--------------------------------"
        print fromResult
        print "----------------------------------WHERE PART-------------------------------"
        print whereResult
        print "---------------------------------GROUP_BY PART----------------------------"
        print groupbyResult
        return (selectResult, fromResult, whereResult, groupbyResult)

    def makeSQLquery(self, select_msg, from_msg, where_msg, groupby_msg):
        query = 'select ' + str(select_msg) + ' from ' + str(from_msg) + ' where ' + str(
            where_msg) + ' group by ' + str(groupby_msg)
        return query

    def getSelectComponent(self, partitionElements, valueElement):
        selectComponentList = []
        for items in partitionElements:
            for i in selectDictionary[items]:
                if (selectDictionary[items][i] == True):
                    selectComponentList.append(tableDictionary[items] + '.' + i)
        print selectComponentList
        for i in selectDictionary[valueElement]:
            if (selectDictionary[valueElement][i] == True):
                selectComponentList.append(
                    i.replace('count(', 'count(distinct ' + str(tableDictionary[valueElement]) + '.'))
        return ','.join(selectComponentList)

    #Function to make tables by recursive calls for tables.
    def makeJoinTable(self, sourceTable, destinationTable, lookup_matrix, occuredTables, Dict):
        if (sourceTable not in occuredTables):
            for i in lookup_matrix[sourceTable][destinationTable]:
                if (i[2] == 'self'):
                    print 'SELF'
                    return
                elif (i[2] == 'direct'):
                    print 'DIRECT'
                    if (destinationTable not in occuredTables):
                        occuredTables.append(destinationTable)
                    if (sourceTable in Dict.keys()):
                        if (destinationTable not in Dict[sourceTable]):
                            Dict[sourceTable].append(destinationTable)
                    else:
                        Dict[sourceTable] = [destinationTable]
                    occuredTables.append(sourceTable)
                    return
                else:
                    if (sourceTable in Dict.keys()):
                        Dict[sourceTable].append(i[2])
                    else:
                        Dict[sourceTable] = [i[2]]
                    occuredTables.append(sourceTable)
                    self.makeJoinTable(i[2], destinationTable, lookup_matrix, occuredTables, Dict)
        else:
            return

    #Function to make FROM component of the sql query
    def getFromComponent(self, partitionElements, valueElement, lookup_matrix):
        partitionTables = []
        for i in partitionElements:
            if (i in categoryDictionary['geographies']):
                partitionTables.insert(0, tableDictionary[i])
            else:
                partitionTables.append(tableDictionary[i])
        majorTablesList = []
        tablesOccuredList = []
        for index, table in enumerate(partitionTables):
            minorTablePath = []
            if table not in self.Dict.keys():
                self.Dict[table] = []
            if (table not in majorTablesList):
                minorTablePath.append(table)
                self.makeJoinTable(table, tableDictionary[valueElement], lookup_matrix, tablesOccuredList, self.Dict)
        majorTablesList = tablesOccuredList
        return ' , '.join(majorTablesList)

    #Function to make whereComponent of the query
    def getWhereComponent(self, partitionElements, valueElement, Dictionary, lookup_matrix):
        whereString = '1=1'
        whereComponentList = [whereString]
        for items in partitionElements:
            if partitionElements[items] != True:
                whereComponentList.append(
                    tableDictionary[items] + '.' + whereDictionary[items] + '=' + partitionElements[items])
        for i in Dictionary:
            for j in Dictionary[i]:
                print str(i) + '.' + str(lookup_matrix[i][j][0][0]) + '=' + str(j) + '.' + str(lookup_matrix[i][j][0][1])
                whereComponentList.append(str(i) + '.' + str(lookup_matrix[i][j][0][0]) + '=' + str(j) + '.' + str(lookup_matrix[i][j][0][1]))
        return ' and '.join(whereComponentList)

    #Function to make GroupBy component of the sql query
    def getGroupByComponent(self, partitionElements, valueElement):
        groupbyComponentList = []
        for items in partitionElements:
            if partitionElements[items] == True:
                groupbyComponentList.append(tableDictionary[items] + '.' + groupbyDictionary[items])
        return ' , '.join(groupbyComponentList)

    # Function to accept query as a string to execute and make dataframe corresponding to that particular query and return that dataframe
    def runQuery(self, query):
        # Make connection with the database
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen_jan15')
        # Making dataframe
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df