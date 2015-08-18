import datetime
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
			vid.video_id as 'Video_ID', 
			v.title as 'Video_Title', 
			vid.non_negotiable as 'Non_Negotiables',
			vid.time_created as 'Data_Entry_Date'
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
		file = '/home/ubuntu/code/dg_git/dg/media/social_website/uploads/non_negotiable.xls'
				
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

		email_list=['all@digitalgreen.org']
		subject = 'Non-Negotiables till '+str(datetime.date.today())
		from_email = 'server@digitalgreen.org'	
		body = """Hi all,

This is a weekly automated email to monitor non-negotiables entry.

Non-negotiables were made mandatory in COCO video form from July. It is important to ensure that correct non-negotiables are being entered by partners. They can also be modified in COCO Admin by DG staff. We hope to show non-negotiables on the website and downloadable cheat sheets next to the corresponding video. 

Please ensure high quality of data entry for Non-negotiables from your respective region.

Thank you for your support!

Tech team
system@digitalgreen.org"""
		for email in email_list:
			if email:
				to_email = email
				msg = EmailMultiAlternatives(subject, body, from_email, [to_email])
				msg.attach_file(file)
				msg.send()



