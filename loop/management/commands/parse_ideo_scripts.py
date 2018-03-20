from django.core.management.base import BaseCommand
from random import sample
import os
import pandas as pd
import pandas.io.sql as psql
import MySQLdb
import dg.settings
from django.db import connection


class Command(BaseCommand):

    def add_arguments(self, parser):

        # to get filenames
        parser.add_argument('filename', help='Enter some filenames', nargs='+', type=str)

        # to parse script type
        parser.add_argument('--referral', '-r', action='store_true', dest='r')
        parser.add_argument('--transport_codes', '-t', action='store_true', dest='t')
        parser.add_argument('--generate_transport_codes', '-g', action='store_true', dest='g')

    def handle(self, *args, **options):
        if options['g']:
            self.generate_transport_codes()
        else:
            for filename in options['filename']:
                if options['r']:
                    self.parse_referral_sheet(filename)
                elif options['t']:
                    self.parse_transport_sheet(filename)

    def parse_referral_sheet(self, filename):
        referral_columns = [u'Name (of referring farmer)', u'Mobile # (of referring farmer)',
                            u'Name (of referred farmer)', u'Mobile # (of referred farmer)']
        columns, parsed_data = self.parse_data(filename)

        if columns is None:
            return
        # validating the data format
        if len(set(columns) & set(referral_columns)) != 4:
            print "Invalid file, please check header or number of columns"
        else:
            # Inserting data into the table
            #referral_query = '''UPDATE loop_farmer
            #                    SET referred_by = %s
            #                    WHERE phone = %s'''

            referral_query = '''INSERT INTO loop_referral (referred_by, referred_farmer, used, time_created)
                                  VALUES (%s, %s, false, now())'''
            # Operations to extract just the required columns,
            # i.e., phone numbers of farmers
            temp_data = [parsed_data[1], parsed_data[3]]
            extracted_data = zip(*temp_data)
            self.run_query_multiple(referral_query, extracted_data)

    def parse_transport_sheet(self, filename):
        referral_columns = [u'Phone Number', u'Free Transport Code', u'Date Used']
        columns, parsed_data = self.parse_data(filename)

        if columns is None:
            return
        # validating the data format
        if len(set(columns) & set(referral_columns)) != 3:
            print "Invalid file, please check header or number of columns"
        else:
            #old_codes, new_codes = self.check_transport_codes(parsed_data[:, 1], parsed_data[:, 0])
            transport_query_insert = '''INSERT INTO loop_farmertransportcode (dateUsed, code, phone)
                                  VALUES (%s, %s, %s)'''

            # Inserting data into the table
            transport_query_update ='''UPDATE loop_farmertransportcode
                                SET dateUsed=%s
                                WHERE code=%s AND phone=%s'''

            # Operations to extract just the required columns,
            # i.e., phone numbers of farmers
            temp_data = [map(str, parsed_data[2]), parsed_data[1], parsed_data[0]]
            extracted_data = zip(*temp_data)
            rows_affected_list = self.run_query_multiple(transport_query_update, extracted_data)
            extracted_data2 = []
            for i, rows_affected in enumerate(rows_affected_list):
                if rows_affected == 0:
                    extracted_data2.append(extracted_data[i])
            self.run_query_multiple(transport_query_insert, extracted_data2)

    def parse_data(self, filename):
        ext_allwd = ['.xlsx', '.xls']
        file_ext = os.path.splitext(filename)[-1]
        if file_ext in ext_allwd or file_ext != '.csv':
            try:
                # Parsing data into list to be inserted
                if file_ext in ext_allwd:
                    print 'Parsing ' + file_ext
                    columns, data = self.parse_excel(filename)
                else:
                    print 'Parsing csv'
                    columns, data = self.parse_csv(filename)
                return columns, data
            except Exception, err:
                print err
                return None, None
        else:
            print "Invalid file format!!"

    def parse_excel(self, filename):
        xl = pd.ExcelFile(filename)
        data = []
        columns = []
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            df = df.dropna(thresh=2)
            data.extend(df.values.tolist())
            columns = df.columns
        return columns, zip(*data)

    def parse_csv(self, filename):
        df = pd.read_csv(filename)
        return df.columns, df.values

    def generate_transport_codes(self):
        # codes start from 10010, no particular reason for selecting this
        codes = sample(range(10010, 20010), 2000)
        transport_code_query = '''INSERT INTO loop_farmertransportcode (code) VALUES (%s)'''
        self.run_query_multiple(transport_code_query, codes)

    def init_cursor(self):
        self.mysql_cn = MySQLdb.connect(host=dg.settings.DATABASES['default']['HOST'],
                                        port=dg.settings.DATABASES['default']['PORT'],
                                        user=dg.settings.DATABASES['default']['USER'],
                                        passwd=dg.settings.DATABASES['default']['PASSWORD'],
                                        db=dg.settings.DATABASES['default']['NAME'],
                                        client_flag=MySQLdb.constants.CLIENT.FOUND_ROWS,
                                        charset='utf8',
                                        use_unicode=True)
        self.cursor = self.mysql_cn.cursor()

    def close_connections(self):
        self.cursor.close()
        self.mysql_cn.commit()
        self.mysql_cn.close()

    def run_query(self, query, args):
        try:
            self.init_cursor()
            self.cursor.execute(query, args)
        except Exception, err:
            print err
        finally:
            self.close_connections()

    def run_query_output(self, query, args):
        try:
            self.init_cursor()
            temp_df = psql.read_sql(query, params=args, con=self.mysql_cn)
            return temp_df
        except Exception, err:
            print err
        finally:
            self.close_connections()
        return None

    def run_query_multiple(self, query, arg_list):
        rows_affected_list = []
        try:
            self.init_cursor()
            for args in arg_list:
                self.cursor.execute(query, args)
                rows_affected_list.append(self.cursor.rowcount)
        except Exception, err:
            print err
        finally:
            self.close_connections()
        return rows_affected_list

    def __init__(self):
        super(Command, self).__init__()
        self.cursor = None
        self.mysql_cn = None
