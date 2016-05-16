import datetime
import xlwt

import MySQLdb

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand

from dg.settings import DATABASES

class Command(BaseCommand):
	def handle(self, *args, **options):
		host = 'localhost'
		user = DATABASES['default']['USER']
		password = DATABASES['default']['PASSWORD']
		database = DATABASES['default']['NAME']

		con = MySQLdb.connect(
			db = database, host=host,
			user=user, passwd=password,
			charset = 'utf8', use_unicode = True)

		mysql = con.cursor()
		mysql.execute("""
			SELECT
				S.training_id as \'Training ID\',
				T.date as \'Date\',
				T.place as \'Place\', 
				L.language_name as \'Language\', 
				A.name as \'Assessment\', 
				count(distinct S.participant_id) as \'Participants Entered\'
			FROM
				training_score S
			JOIN
				training_training T on T.id = S.training_id
			JOIN
				videos_language L on L.id = T.language_id
			JOIN
				training_assessment A on A.id = T.assessment_id
			GROUP BY
				training_id;
		""")

		fields = mysql.fetchall()
		field_hdrs = [i[0] for i in mysql.description]

		file = '/Users/jahnavi/dg/dg/media/social_website/uploads/emails/training_data.xls'
		#file = '/home/ubuntu/code/dg_git/dg/media/social_website/uploads/loop_data.xls'

		wb = xlwt.Workbook()
		ws = wb.add_sheet('Training Data Summary')
		style = xlwt.easyxf('font: bold 1')
		col_widths = [15,15,15,15,15,15,15]
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

		#email_list=['bihar@digitalgreen.org', 'namita@digitalgreen.org', 'charu@digitalgreen.org', 'aditya@digitalgreen.org']
		email_list=['jahnavi@digitalgreen.org']
		subject = 'Training: Data received till '+str(datetime.date.today())
		from_email = 'server@digitalgreen.org'
		body = """Hi Everyone,

This is a daily automated email to monitor training data entry.

This mail is to keep you updated on the progress in data entry and keep check on quality of entered data. 

Thank you for your support!

Tech team
system@digitalgreen.org"""
		for email in email_list:
			if email:
				to_email = email
				msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
				msg.attach_file(file)
				msg.send()



