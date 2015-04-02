__author__ = 'Lokesh'

import os.path
from configuration import tableDictionary, whereDictionary, selectDictionary, groupbyDictionary, categoryDictionary, orderDictionary
import pandas as pd
import MySQLdb
import pandas.io.sql as psql
import csv
import dg.settings

class data_lib():
    Dict = {}
    lookup_matrix = {}

    # Accepts options i.e. dictionary of dictionary e.g. {'partition':{'partner':'','state',''},'value':{'nScreening':True,'nAdoption':true}}
    # This function is responsible to call function for checking validity of input and functions to make dataframes according to the inputs
    def handle_controller(self, args, options):
        print options
        self.lookup_matrix = self.read_lookup_csv()
        relevantPartitionDictionary = {}
        relevantValueDictionary = {}
        # --- checking validity of the partition fields and value fields entered by user ---
        if self.check_partitionfield_validity(options['partition']):
            for item in options['partition']:
                if options['partition'][item] != False:
                    relevantPartitionDictionary[item] = options['partition'][item]
        else:
            print "Warning - Invalid input for partition fields"

        if self.check_valuefield_validity(options['value']):
            for item in options['value']:
                if item =='list' and options['value']['list'] != False:
                    relevantValueDictionary[options['value'][item]] = True
                    relevantPartitionDictionary[categoryDictionary['partitionCumValues'][options['value'][item]]] = False
                    del relevantPartitionDictionary[categoryDictionary['partitionCumValues'][options['value'][item]]]
                if options['value'][item] != False and item!='list':
                    relevantValueDictionary[item] = options['value'][item]
        else:
            print "Warning - Invalid input for Value fields"

        final_df = pd.DataFrame()

        for input in relevantValueDictionary:
            queryComponents = self.getRequiredTables(relevantPartitionDictionary, input, args, self.lookup_matrix)
    #        print "----------------------------------Full SQL Query---------------------------"
            query = self.makeSQLquery(queryComponents[0], queryComponents[1], queryComponents[2], queryComponents[3], queryComponents[4])
    #        print query
    #        print "-------------------------------Result--------------------------------"
            df = self.runQuery(query)
            if final_df.empty:
                final_df = df
            else:
                final_df = pd.merge(final_df, df, how='outer')
    #        print df
        resultant_df = self.order_data(final_df)
        return resultant_df

    def order_data(self, dataframe):
        header = dataframe.columns.tolist()
        ordered_cols = [None]*len(orderDictionary)
        for col in header:
            if col not in orderDictionary.keys():
                ordered_cols.append(col)
            else:
                ordered_cols[orderDictionary[col]] = col
        ordered_cols = filter(lambda a: a != None, ordered_cols)
        dataframe = dataframe[ordered_cols]
        return dataframe

    def read_lookup_csv(self):
        file_data = csv.reader(open(os.path.join(dg.settings.MEDIA_ROOT + r'/raw_data_analytics/data_analytics.csv')))
        headers = next(file_data)
        headers.remove('')
        matrix = {}
        for row in file_data:
            sub_matrix = {}
            for i in range(0, len(headers)):
                sub_matrix[headers[i]] = []
                temp = row[i + 1].split('$')
                for t in temp:
                    if '&' in t:
                        andtemp = t.split('&')
                        for vl in andtemp:
                            sub_matrix[headers[i]].append(tuple(vl.split('#')))
                    else:
                        sub_matrix[headers[i]].append(tuple(t.split('#')))
            matrix[row[0]] = sub_matrix
        return matrix

    # Function to check validity of the partition field inputs by user by comparing with the generalPartitionList
    def check_partitionfield_validity(self, partitionField):
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

    def getRequiredTables(self, partitionDict, valueDictElement, args, lookup_matrix):
        self.Dict.clear()
        selectResult = self.getSelectComponent(partitionDict, valueDictElement)
        fromResult = self.getFromComponent(partitionDict, valueDictElement, lookup_matrix)
        whereResult = self.getWhereComponent(partitionDict, valueDictElement, self.Dict, args, lookup_matrix)
        groupbyResult = self.getGroupByComponent(partitionDict, valueDictElement)
        orderbyResult = self.getOrderByComponent(partitionDict, valueDictElement)
        #print "----------------------------------SELECT PART------------------------------"
        #print selectResult
        #print "----------------------------------FROM PART--------------------------------"
        #print fromResult
        #print "----------------------------------WHERE PART-------------------------------"
        #print whereResult
        #print "---------------------------------GROUP_BY PART----------------------------"
        #print groupbyResult
        return (selectResult, fromResult, whereResult, groupbyResult, orderbyResult)

    def makeSQLquery(self, select_msg, from_msg, where_msg, groupby_msg, orderby_msg):
        query = 'select ' + str(select_msg) + ' from ' + str(from_msg) + ' where ' + str(
            where_msg) + ' group by ' + str(groupby_msg) + ' order by ' + str(orderby_msg)
        return query

    def getSelectComponent(self, partitionElements, valueElement):
        selectComponentList = []
        for items in partitionElements:
            for i in selectDictionary[items]:
                if (selectDictionary[items][i] == True):
                    selectComponentList.append(tableDictionary[items] + '.' + i + ' AS ' + items)
        for i in selectDictionary[valueElement]:
            if (selectDictionary[valueElement][i] == True):
                x = ['count','distinct']
                if all(a in i for a in x):
                    selectComponentList.append(
                            i.replace('count(distinct', 'count(distinct ' + str(tableDictionary[valueElement]) + '.') + ' AS ' + 'Unique_'+valueElement)
                elif "count" in i and "distinct" not in i:
                    selectComponentList.append(i.replace('count(','count('+str(tableDictionary[valueElement])+'.') + ' AS ' + valueElement)
                elif "distinct" in i and "count" not in i:
                    selectComponentList.insert(0,(i.replace('distinct(',' distinct('+str(tableDictionary[valueElement])+'.') + ' AS ' + valueElement))
                else:
                    selectComponentList.append(str(tableDictionary[valueElement]) + '.' + i + ' AS ' + valueElement)
        return ','.join(selectComponentList)

    # Function to make tables by recursive calls for tables.
    def makeJoinTable(self, sourceTable, destinationTable, lookup_matrix, occuredTables, Dict):
        if (sourceTable not in occuredTables):
            for i in lookup_matrix[sourceTable][destinationTable]:
                if (i[2] == 'self'):
                    return
                elif (i[2] == 'direct'):
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

    # Function to make FROM component of the sql query
    def getFromComponent(self, partitionElements, valueElement, lookup_matrix):
        partitionTables = []
        for i in partitionElements:
            if (i in categoryDictionary['geographies']):
                partitionTables.insert(0, tableDictionary[i])
            else:
                partitionTables.append(tableDictionary[i])
        majorTablesList = []
        tablesOccuredList = []
        counter = 0
        for index, table in enumerate(partitionTables):
            minorTablePath = []
            if table not in self.Dict.keys():
                self.Dict[table] = []
            if (table not in majorTablesList):
                minorTablePath.append(table)
                self.makeJoinTable(table, tableDictionary[valueElement], lookup_matrix, tablesOccuredList, self.Dict)
            counter+=1
        majorTablesList = tablesOccuredList

        if not partitionElements:
            if valueElement in categoryDictionary['partitionCumValues'].keys():
                majorTablesList.append(tableDictionary[valueElement])
        return ' , '.join(majorTablesList)


    # Function to make whereComponent of the query
    def getWhereComponent(self, partitionElements, valueElement, Dictionary, args, lookup_matrix):
        whereString = '1=1'
        whereComponentList = [whereString]
        for items in partitionElements:
            if partitionElements[items] != True:
                whereComponentList.append(
                    tableDictionary[items] + '.' + whereDictionary[items] + '=' + partitionElements[items])
        for i in Dictionary:
            for j in Dictionary[i]:
                for k in range(0,len(lookup_matrix[i][j])):
                    whereComponentList.append(str(i) + '.' + str(lookup_matrix[i][j][k][0]) + '=' + str(j) + '.' + str(lookup_matrix[i][j][k][1]))
        if '.' in str(whereDictionary[valueElement]):
            whereComponentList.append(str(whereDictionary[valueElement]) + ' between \'' + str(args[0]) + '\' and \'' + str(args[1]) + '\'')
        else:
            whereComponentList.append(
                str(tableDictionary[valueElement]) + '.' + str(whereDictionary[valueElement]) + ' between \'' + str(
                    args[0]) + '\' and \'' + str(args[1]) + '\'')
        return ' and '.join(whereComponentList)

    # Function to make GroupBy component of the sql query
    def getGroupByComponent(self, partitionElements, valueElement):
        groupbyComponentList = ['1']
        for items in partitionElements:
            if partitionElements[items] != False:
                groupbyComponentList.append(tableDictionary[items] + '.' + groupbyDictionary[items])
        if groupbyDictionary[valueElement] != False:
            groupbyComponentList.append(tableDictionary[valueElement] + '.' + str(groupbyDictionary[valueElement]))
        return ' , '.join(groupbyComponentList)

    # Function to make OrderBy component of the sql query
    def getOrderByComponent(self, partitionElements, valueElements):
        orderbyComponentList = ['1']
        ordered_cols = [None]*len(orderDictionary)
        for items in partitionElements:
            if partitionElements[items] != False:
                ordered_cols[orderDictionary[items]] = items
        ordered_cols = filter(lambda a: a != None, ordered_cols)
        orderbyComponentList += ordered_cols
        return ' , '.join(orderbyComponentList)

    # Function to accept query as a string to execute and make dataframe corresponding to that particular query and return that dataframe
    def runQuery(self, query):
        # Make connection with the database
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd=dg.settings.DATABASES['default']['PASSWORD'], db=dg.settings.DATABASES['default']['NAME'])
        # Making dataframe
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df