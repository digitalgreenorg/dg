__author__ = 'Lokesh'
from optparse import make_option

from django.core.management.base import BaseCommand

from raw_data_analytics.utils.configuration import tableDictionary, whereDictionary, selectDictionary


class Command(BaseCommand):

    # Description for the tablesDictionary
    # key - possible field names that can be included in the partition field.
    # value - (table_name to be used, <symbol> to be used while making query for data extraction)
    # tablesDictionary = {'partner': ('programs_partner', 'P'), 'country': ('geographies_country', 'C'),
    #                     'state': ('geographies_state', 'S'), 'district': ('geographies_district', 'D'),
    #                     'block': ('geographies_block', 'B'), 'village': ('geographies_village', 'V'),
    #                     'mediator': ('people_mediator','M'), 'adoption':('activities_personadoptpractice','PAP'),
    #                     'person_attending': ('activities_personmeetingattendance','PMA'),'video':('videos_video','VV'),
    #                     'screening': ('activites_screening','SC'),'people':('people_person','PP')}
    #
    # Description for generalPartitionList Dictionary ---
    # key - column to be included as partition field in dataframe
    # value - False - default value
    # partition_list_all = {'partner': False, 'country': False, 'state': False, 'district': False, 'block': False,
    #                         'village': False,'mediator': False, 'video': False, 'practice': False, 'practiceSector': False}

    # Description for generalValueList Dictionary---
    # key - Column to be included as Value field in dataframe
    # value - function name which is being used to make query for the data extraction corresponding to the key
    # value_list_all = {'nScreening': 'nScreeningDF', 'nAdoption': 'nAdoptionDF'}
    #
    # category_all = {'geographies':False, 'people':False, 'video':False, 'activities':False}
    #
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
        # make_option('-f', '--video',
        #             action='store',
        #             default=False,
        #             dest='video',
        #             help='Takes video name as input for filter'),
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
        self.handle_controller(args, options)

    # def make_query_components(self, options):
    #     print options
    #     gflag = 0
    #     sflag = 0
    #     groupbyClause = ''
    #     whereClause = " 1=1 "
    #     selectClause = ''
    #
    #     """ Add similar IF block for any new partition field and to add in groupbyClause, selectClause and whereClause """
    #
    #     # If section to check if user has selected partner for partition field/filter field
    #     if (options['partner'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['partner'][1] + '.partner_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['partner'][1] + '.partner_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['partner'][1] + '.partner_name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['partner'][1] + '.partner_name'
    #
    #         if (options['partner'] != True):
    #             whereClause += "and " + self.tablesDictionary['partner'][1] + ".partner_name=\'" + options[
    #                 'partner'] + "\'"
    #
    #     # If section to check if user has selected country for partition field/filter field
    #     if (options['country'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['country'][1] + '.country_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['country'][1] + '.country_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['country'][1] + '.country_name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['country'][1] + '.country_name'
    #
    #         if (options['country'] != True):
    #             whereClause += "and " + self.tablesDictionary['country'][1] + ".country_name=\'" + options[
    #                 'country'] + "\'"
    #
    #     # If section to check if user has selected state for partition field/filter field
    #     if (options['state'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['state'][1] + '.state_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['state'][1] + '.state_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['state'][1] + '.state_name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['state'][1] + '.state_name'
    #
    #         if (options['state'] != True):
    #             whereClause += "and " + self.tablesDictionary['state'][1] + ".state_name=\'" + options['state'] + "\'"
    #
    #     # If section to check if user has selected district for partition field/filter field
    #     if (options['district'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['district'][1] + '.district_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['district'][1] + '.district_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['district'][1] + '.district_name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['district'][1] + '.district_name'
    #
    #         if (options['district'] != True):
    #             whereClause += "and " + self.tablesDictionary['district'][1] + ".district_name=\'" + options[
    #                 'district'] + "\'"
    #
    #     # If section to check if user has selected block for partition field/filter field
    #     if (options['block'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['block'][1] + '.block_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['block'][1] + '.block_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['block'][1] + '.block_name '
    #         else:
    #              sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['block'][1] + '.block_name'
    #
    #         if (options['block'] != True):
    #             whereClause += "and " + self.tablesDictionary['block'][1] + ".block_name=\'" + options['block'] + "\'"
    #
    #     # If section to check if user has selected village for partition field/filter field
    #     if (options['village'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['village'][1] + '.village_name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['village'][1] + '.village_name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['village'][1] + '.village_name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['village'][1] + '.village_name'
    #
    #         if (options['village'] != True):
    #             whereClause += "and " + self.tablesDictionary['village'][1] + ".village_name=\'" + options[
    #                 'village'] + "\'"
    #
    #     # If section to check if user has selected mediator for partition field/filter field
    #     if (options['mediator'] != False):
    #         if gflag == 1:
    #             groupbyClause += ',' + self.tablesDictionary['mediator'][1] + '.name'
    #         else:
    #             gflag = 1
    #             groupbyClause = ' group by ' + self.tablesDictionary['mediator'][1] + '.name'
    #         if sflag == 1:
    #             selectClause += ',' + self.tablesDictionary['mediator'][1] + '.name '
    #         else:
    #             sflag = 1
    #             selectClause = ' ' + self.tablesDictionary['mediator'][1] + '.name'
    #
    #         if (options['mediator'] != True):
    #             whereClause += "and " + self.tablesDictionary['mediator'][1] + ".name=\'" + options[
    #                 'mediator'] + "\'"

        # def country_sql()
        #     select_fld = 'adoptions''
        #     select_fld = 'a.adoptions/a.screenings'
        #     return selectFlds, whereCLasue, GroupByClause
        #
        # ptn = 'country'
        # clauses = ""
        # for ptn in ptns:
        #     clauses.append(partition_dict[ptn][2]
        #
        # select_query = 'SELECT' + AND '.clauses[0]
        #
        # grp_qry = ""
        # if len(grp_flds) > 1
        #     grp_qry = GROUP BY'' + ' AND '
        # sql_query = """
        # SELECT {select_qry}
        # FROM
        #   {join_qry}
        # {where_qry}
        # """
        #
        # return [selectClause, whereClause, groupbyClause]

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

    # Function to accept query as a string to execute and make dataframe corresponding to that particular query and return that dataframe





    # def runQuery(self, query):
    #     # Make connection with the database
    #     mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
    #     # Making dataframe
    #     temp_df = psql.read_sql(query, con=mysql_cn)
    #     mysql_cn.close()
    #     return temp_df
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

    def handle_controller(self, args, options):
        # Accepts options i.e. dictionary of dictionary e.g. {'partition':{'partner':'','state',''},'value':{'nScreening':True,'nAdoption':true}}
        # This function is responsible to call function for checking validity of input and functions to make dataframes according to the inputs
        print "options is ---------"
        print options
        print "$$$$$$$$$$$$$$$$$$$"
        value_list_to_find = []
        relevantPartitionDictionary={}
        relevantValueDictionarys={}

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
                    relevantValueDictionarys[item] = options['value'][item]
        else:
            print "Warning - Invalid input for Value fields"

        for input in relevantValueDictionarys:
            queryComponents = getRequiredTables(relevantPartitionDictionary,input)
            print queryComponents
        return 0

    def getSelectComponent(partitionElements,valueElement):
        selectComponentList = []
        for items in partitionElements:
            selectComponentList.append(selectDictionary[items])
        print selectComponentList
        return ','.join(selectComponentList)


    def getFromComponent(partitionElements,valueElement):
        print 'testing From Component'

    def getWhereComponent(partitionElements,valueElement):
        whereString = '1=1'
        whereComponentList = []
        for items in partitionElements:
            if partitionElements[items]!=True:
                whereComponentList.append(whereDictionary[items] + '=' + partitionElements[items])
        print whereComponentList
        return ' and '.join(whereComponentList)

    def getGroupByComponent(partitionElements,valueElement):
        print 'testing GroupBy Component'

    def getRequiredTables(partitionDict, valueDictElement):
        selectResult = getSelectComponent(partitionDict, valueDictElement)
        fromResult = getFromComponent(partitionDict,valueDictElement)
        whereResult = getWhereComponent(partitionDict, valueDictElement)
        groupbyResult = getGroupByComponent(partitionDict, valueDictElement)
        return 'GetRequiredTables function got over where'

    #         for element in options['partition'].key:
    #             tablesList = tableDictionary[element]queryComponents = (options['partition'])
    #         if self.check_valuefield_validity(options['value']):
    #             for k, v in options['value'].items():
    #                 if v:
    #                     value_list_to_find.append(k)
    #         else:
    #             print "Check the value field inputs again"
    #     else:
    #         print "Check the partition field inputs again"
    #     # --- checking of validity ends here ---
    #
    #     # --- creation of dataframe begins here ----
    #     df = pd.DataFrame()
    #     for element in value_list_to_find:
    #         call_function = getattr(self, self.generalValueList[element])
    #         if df.empty:
    #             df = df.append(call_function(queryComponents[0], queryComponents[1], queryComponents[2], args[0], args[1]))
    #         else:
    #             df = pd.merge(df, call_function(queryComponents[0], queryComponents[1], queryComponents[2], args[0], args[1]),
    #                           how='outer')
    #     # --- creation of dataframe ends here ---
    #     print df
    #     self.make_excel(df)
    #
    # def make_excel(self,df):
    #     df.to_excel('library_data.xlsx','Sheet1')
    #
    # # This function is not being used for now but not being removed for future reference. Will be erased in production mode
    # def home(self, selectClause, whereClause, groupbyClause):
    #     # Make query to extract data and create dataframe for further processing
    #     # print 'loaded dataframe from MySQL. records:', len(df_mysql)
    #     print "################################"
    #
    # def make_from_part(self, options):
    #     if(options['partner']):
    #         join_tables_list = [self.tablesDictionary['partner'][0]]
