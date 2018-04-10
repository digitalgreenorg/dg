from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

import pandas as pd
import pandas.io.sql as psql
import MySQLdb
import dg.settings
import csv
import datetime
from datetime import timedelta

class Command(BaseCommand):

    def send_mail(self,gender_wise_farmer):
        till_date = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = "Gender wise counting of farmers who have used the LOOP platform at least once in Bangladesh: Data till %s"%(till_date)
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['suprita@digitalgreen.org', 'tech@digitalgreen.org']
        body = ['Dear Team,\n\nBelow is the genderwise counting of farmers who have used the LOOP platform at least once in Bangladesh.\n\n',
                'Common Active farmer who participated in YEAR 1 as well as YEAR 2: %s\n\tNo of Female Farmers: %s\n\tNo of Male Farmers: %s\n\n'%(gender_wise_farmer['F'][0]+ gender_wise_farmer['M'][0],gender_wise_farmer['F'][0], gender_wise_farmer['M'][0]),
                'New Farmer who participated in YEAR 2 but not in YEAR 1: %s\n\tNo of Female Farmers: %s\n\tNo of Male Farmers: %s\n\n'%(gender_wise_farmer['F'][1]+gender_wise_farmer['M'][1],gender_wise_farmer['F'][1],gender_wise_farmer['M'][1]),
                'Please contact system@digitalgreen.org for any question or clarification.\n\nThank you.']
        body = ''.join(body)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.send()

    def run_query(self,query):
        mysql_cn = MySQLdb.connect(host=dg.settings.DATABASES['default']['HOST'], port=dg.settings.DATABASES['default']['PORT'],
            user=dg.settings.DATABASES['default']['USER'] ,
            passwd=dg.settings.DATABASES['default']['PASSWORD'],
            db=dg.settings.DATABASES['default']['NAME'],
            charset = 'utf8',
            use_unicode = True)
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df

    def handle(self, *args, **options):

        # Send stats one day before last Tuesday of Month (Monday).
        current_time = datetime.datetime.now()
        # Check If today is Monday
        if current_time.weekday() == 0:
            # Check if This is Monday before last Tuesday.
            current_month = current_time.month
            tuesday_count = 0
            next_date = current_time + timedelta(days=1)
            while next_date.month == current_month:
                if next_date.weekday() == 1:
                    tuesday_count += 1
                next_date = next_date + timedelta(days=1)
            # If there is only on Tuesday after this monday in this month, then send stats.
            if tuesday_count == 1:
                # Query for Common Active farmer who participated and YEAR 1 (1 Oct 2016 - 30 Sept 2017)
                # as well as YEAR 2 (1 Oct 2017 - 30 Sept 2018)
                gender_wise_common_active_farmer_query = '''SELECT 
                        lf.gender, COUNT(DISTINCT lf.id) 'count'
                    FROM
                        loop_combinedtransaction lc1
                            JOIN
                        loop_farmer lf ON lf.id = lc1.farmer_id
                            JOIN
                        loop_village lv ON lv.id = lf.village_id
                            JOIN
                        loop_block lb ON lb.id = lv.block_id
                            JOIN
                        loop_district ld ON ld.id = lb.district_id
                            JOIN
                        loop_state ls ON ls.id = ld.state_id
                    WHERE
                        ls.country_id = 2
                            AND lc1.date >= 20171001
                            AND lc1.farmer_id IN (SELECT 
                                lc2.farmer_id
                            FROM
                                loop_combinedtransaction lc2
                                    JOIN
                                loop_farmer lf ON lf.id = lc2.farmer_id
                                    JOIN
                                loop_village lv ON lv.id = lf.village_id
                                    JOIN
                                loop_block lb ON lb.id = lv.block_id
                                    JOIN
                                loop_district ld ON ld.id = lb.district_id
                                    JOIN
                                loop_state ls ON ls.id = ld.state_id
                            WHERE
                                ls.country_id = 2
                                    AND lc2.date >= 20161001
                                    AND lc2.date <= 20170930)
                    GROUP BY lf.gender'''

                # Query for New Farmer who participated in YEAR 2 but not in YEAR 1
                gender_wise_new_farmer_year2_query ='''SELECT 
                        lf.gender, COUNT(DISTINCT lf.id) 'count'
                    FROM
                        loop_combinedtransaction lc1
                            JOIN
                        loop_farmer lf ON lf.id = lc1.farmer_id
                            JOIN
                        loop_village lv ON lv.id = lf.village_id
                            JOIN
                        loop_block lb ON lb.id = lv.block_id
                            JOIN
                        loop_district ld ON ld.id = lb.district_id
                            JOIN
                        loop_state ls ON ls.id = ld.state_id
                    WHERE
                        ls.country_id = 2
                            AND lc1.date >= 20171001
                            AND lc1.farmer_id NOT IN (SELECT 
                                lc2.farmer_id
                            FROM
                                loop_combinedtransaction lc2
                                    JOIN
                                loop_farmer lf ON lf.id = lc2.farmer_id
                                    JOIN
                                loop_village lv ON lv.id = lf.village_id
                                    JOIN
                                loop_block lb ON lb.id = lv.block_id
                                    JOIN
                                loop_district ld ON ld.id = lb.district_id
                                    JOIN
                                loop_state ls ON ls.id = ld.state_id
                            WHERE
                                ls.country_id = 2
                                    AND lc2.date >= 20161001
                                    AND lc2.date <= 20170930)
                    GROUP BY lf.gender'''
                gender_wise_common_active_farmer_df = self.run_query(gender_wise_common_active_farmer_query)

                gender_wise_new_farmer_year2_df = self.run_query(gender_wise_new_farmer_year2_query)
                gender_wise_farmer = dict()
                gender_wise_farmer[gender_wise_common_active_farmer_df.iloc[0]['gender']] = (gender_wise_common_active_farmer_df.iloc[0]['count'],gender_wise_new_farmer_year2_df.iloc[0]['count'])
                gender_wise_farmer[gender_wise_common_active_farmer_df.iloc[1]['gender']] = (gender_wise_common_active_farmer_df.iloc[1]['count'],gender_wise_new_farmer_year2_df.iloc[1]['count'])
                self.send_mail(gender_wise_farmer)
