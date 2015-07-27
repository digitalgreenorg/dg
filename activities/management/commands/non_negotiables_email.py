import datetime
import csv
import xlwt

import MySQLdb

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	def handle(self, *args, **options):		
		host = 'localhost'
		user = 'root'
		password = '#0.Green11017.'
		database = 'digitalgreen'

		con = MySQLdb.connect(
			db = database, host=host, 
			user=user, passwd=password, 
			charset = 'utf8', use_unicode = True)

		mysql = con.cursor()
		mysql.execute("""
		SELECT
			c.country_name as 'Country',
			s.state_name as 'State',
			P.partner_name as 'Partner',
			vid.video_id as 'Video ID', 
			v.title as 'Video Title', 
			vid.non_negotiable as 'Non-Negotiables',
			vid.time_created as 'Created Date'
		FROM 
			videos_nonnegotiable vid
			join videos_video v on v.id = vid.video_id
			join programs_partner P on P.id = v.partner_id
			join geographies_village Vl on Vl.id = v.village_id
			join geographies_block b on b.id = Vl.block_id
			join geographies_district d on d.id = b.district_id
			join geographies_state s on s.id = d.state_id
			join geographies_country c on c.id = s.country_id
		order by c.id, s.id, P.id, v.id;
		""")

		fields = mysql.fetchall()
		field_hdrs = [i[0] for i in mysql.description]

		#file = 'C:/Users/Abhishek/Documents/dg/dg/media/social_website/uploads/non_negotiable.xls'
		file = '/home/ubuntu/code/dg_git/dg/media/social_website/uploads/non_negotiable.csv'
				
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Sheet1')
		style = xlwt.easyxf('font: bold 1')
		col_widths = [10,10,10,10,50,50,15]
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

		email_list=['abhishekchandran@digitalgreen.org','aditya@digitalgreen.org']
		subject = 'NonNegotiables entered till '+str(datetime.date.today())
		from_email = 'server@digitalgreen.org'	
		body = 'PFA'
		for email in email_list:
			if email:
				to_email = email
				msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
				msg.attach_file(file)
				msg.send()



