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
				S.training_id AS \'Training ID\',
				T.date AS \'Date\',
				T.place AS \'Place\', 
				TR.name AS \'Trainer\',
				L.language_name AS \'Language\', 
				A.name AS \'Assessment\', 
				COUNT(distinct S.participant_id) as \'Participants Entered\'
			FROM
				training_score S
			JOIN
				training_training T ON T.id = S.training_id
			JOIN
				videos_language L ON L.id = T.language_id
			JOIN
				training_assessment A ON A.id = T.assessment_id
			JOIN
				training_training_trainer TTT ON TTT.training_id = T.id
			JOIN
				training_trainer TR ON TR.id = TTT.trainer_id
			GROUP BY
				S.training_id;
		""")

		mysql1 = con.cursor()
		mysql1.execute("""
			SELECT 
   				S.training_id AS \'Training ID\',
   				TR.name AS \'Trainer\', 
   				A.name AS \'Participant\', 
   				COUNT(S.score) AS \'Score\'
			FROM
    			training_score S
        	LEFT JOIN
    			training_training_trainer TT ON TT.training_id = S.training_id
        	LEFT JOIN
    			training_trainer TR ON TR.id = TT.trainer_id
        	LEFT JOIN
    			people_animator A ON S.participant_id = A.id
			WHERE
    			S.score > 0
			GROUP BY 
				A.id, 
				TR.id, 
				S.training_id
			ORDER BY 
				S.training_id DESC, 
				TR.name, 
				A.name;
		""")

		fields = mysql.fetchall()
		field_hdrs = [i[0] for i in mysql.description]

		#file = '/Users/jahnavi/dg/dg/media/social_website/uploads/emails/training_data.xls'
		file = '/home/ubuntu/code/dg_git/dg/media/social_website/uploads/training_data.xls'

		wb = xlwt.Workbook()
		ws = wb.add_sheet('Training Data Summary')
		style = xlwt.easyxf('font: bold 1')
		col_widths = [10,10,20,20,10,20,18]
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

		fields = mysql1.fetchall()
		field_hdrs = [i[0] for i in mysql1.description]

		ws1 = wb.add_sheet('Participant Scores')
		style = xlwt.easyxf('font: bold 1')
		col_widths = [10,20,25,6]
		date_xf = xlwt.easyxf(num_format_str='DD/MM/YYYY') # sets date format in Excel

		for i,hdr in enumerate(field_hdrs):
			ws1.write(0, i, hdr, style)
			ws1.col(i).width = 256 * col_widths[i] #char_size*num_chars

		for i, row in enumerate(fields):
			i += 1
			for j, cell in enumerate(row):
				if isinstance(cell, datetime.date):
					ws1.write(i, j, cell, date_xf)
				else:
					ws1.write(i, j, cell)
		wb.save(file)

		email_list = ['bihar@digitalgreen.org', 'namita@digitalgreen.org', 'charu@digitalgreen.org', 'aditya@digitalgreen.org', 'tanmaygoel@digitalgreen.org', 'jahnavi@digitalgreen.org', 'smriti@digitalgreen.org']
		#email_list=['jahnavi@digitalgreen.org']
		subject = 'Training: Data received till '+str(datetime.date.today())
		from_email = 'server@digitalgreen.org'
		body = """Hi Everyone,

This is a weekly automated email to monitor training data entry.

This mail is to keep you updated on the progress in data entry. 


Thank you for your support!

Tech team
system@digitalgreen.org"""
		for email in email_list:
			if email:
				to_email = email
				msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
				msg.attach_file(file)
				msg.send()



