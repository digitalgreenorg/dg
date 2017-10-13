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
        to_email = ['kellystenhoff@digitalgreen.org', 'tech@digitalgreen.org']
        body = ['Dear Team,\n\nBelow is the genderwise counting of farmers who have used the LOOP platform at least once in Bangladesh.\n\n',
                'No of Female Farmers: %s\nNo of Male Farmers: %s\n\n'%(gender_wise_farmer['F'], gender_wise_farmer['M']),
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
                gender_wise_bangladesh_farmer_query = '''SELECT 
                        lf.gender, COUNT(DISTINCT lf.id) 'count'
                    FROM
                        loop_combinedtransaction lc
                            JOIN
                        loop_farmer lf ON lf.id = lc.farmer_id
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
                    GROUP BY lf.gender
                '''
                gender_wise_bangladesh_farmer_df = self.run_query(gender_wise_bangladesh_farmer_query)
                gender_wise_farmer = dict()
                gender_wise_farmer[gender_wise_bangladesh_farmer_df.iloc[0]['gender']] = gender_wise_bangladesh_farmer_df.iloc[0]['count']
                gender_wise_farmer[gender_wise_bangladesh_farmer_df.iloc[1]['gender']] = gender_wise_bangladesh_farmer_df.iloc[1]['count']
                self.send_mail(gender_wise_farmer)
