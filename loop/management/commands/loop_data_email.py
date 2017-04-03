import datetime
import xlwt

import MySQLdb

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand

from dg.settings import DATABASES

class Command(BaseCommand):
	def handle(self, *args, **options):
		host = DATABASES['default']['HOST']
		user = DATABASES['default']['USER']
		password = DATABASES['default']['PASSWORD']
		database = DATABASES['default']['NAME']
		port = DATABASES['default']['PORT']

		con = MySQLdb.connect(
			db = database, host=host,
			user=user, passwd=password, port=port,
			charset = 'utf8', use_unicode = True)

		mysql = con.cursor()
		mysql.execute("""
            SELECT
                LCT.date as \'Date\',
                LP.name as \'Aggregator Name\',
                AU.username as \'Aggregator Phone Number\',
                LF.name as \'Farmer Name\',
                LV.village_name as \'Farmers Village Name\',
                LB.block_name as \'Block Name\',
                LD.district_name as \'District Name\',
                LM.mandi_name as \'Mandi Name\',
                LC.crop_name as \'Crop Name\',
                LCT.quantity as \'Quantity\',
                LCT.price as \'Price\',
                LCT.amount as \'Amount\',
                LCT.status as \'Payment Status\'
            FROM
                loop_combinedtransaction LCT,
                loop_farmer LF,
                loop_village LV,
                loop_block LB,
                loop_district LD,
                loop_crop LC,
                loop_mandi LM,
                loop_loopuser LP,
                auth_user AU
            WHERE
                LCT.farmer_id = LF.id
                    AND LCT.crop_id = LC.id
                    AND LCT.mandi_id = LM.id
                    AND LCT.user_created_id = LP.user_id
                    AND LP.user_id = AU.id
                    AND LF.village_id = LV.id
                    AND LV.block_id = LB.id
                    AND LB.district_id = LD.id
            ORDER BY LCT.date DESC;
		""")

		fields = mysql.fetchall()
		field_hdrs = [i[0] for i in mysql.description]

		#file = 'C:/Users/Server-Tech/Documents/dg_clone/dg/media/social_website/uploads/emails/loop_data.xls'
		file = '/home/ubuntu/code/dg_git/dg/media/social_website/uploads/emails/loop_data.xls'

		wb = xlwt.Workbook()
		ws = wb.add_sheet('Sheet1')
		style = xlwt.easyxf('font: bold 1')
		col_widths = [15,15,15,15,15,15,15,15,15,15,15,15,15]
		date_xf = xlwt.easyxf(num_format_str='DD/MM/YYYY') # sets date format in Excel

		for i,hdr in enumerate(field_hdrs):
			ws.write(0, i, hdr, style)
			ws.col(i).width = 256 * col_widths[i] #char_size*num_chars

		for i, row in enumerate(fields):
			i += 1
			for j, cell in enumerate(row):
				if isinstance(cell, datetime.date):
					ws.write(i, j, cell, date_xf)
				else:
					ws.write(i, j, cell)
		wb.save(file)

		email_list=['loop@digitalgreen.org', 'sujit@digitalgreen.org']
		subject = 'LOOP: Data received till '+str(datetime.date.today())
		from_email = 'server@digitalgreen.org'
		body = """Hi Everyone,

This is a daily automated email to monitor loop data entry.

Aggregators are entering data through the LOOP mobile app from end of January 2016. It is important to be updated and keep track of data being entered by the aggregators in the mobile app.

Therefore, this mail is to keep you updated on the progress in data entry and keep check on quality of entered data.

Thank you for your support!

Tech team
system@digitalgreen.org"""
		for email in email_list:
			if email:
				to_email = email
				msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
				msg.attach_file(file)
				msg.send()
