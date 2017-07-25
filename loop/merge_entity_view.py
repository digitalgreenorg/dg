import os
import csv
import time
import datetime
import pandas as pd
import numpy as np

from django.db import transaction
from django.core.mail.message import EmailMessage
from django.db.models import get_model
from dg.settings import MEDIA_ROOT, EMAIL_HOST_USER
from pytz import timezone

from loop.models import Farmer, CombinedTransaction, Gaddidar, GaddidarCommission, GaddidarShareOutliers
from loop import mergeentityconfig as cnf

df = pd.DataFrame()

def save_file(merge_file):
	merge_file_name = "MergeEntities_" + str(datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y_%m_%d_%H_%M_%S_%f')) + '.xlsx'
	merge_file_path =  MEDIA_ROOT + "\\loop\\merge_entity\\" + merge_file_name
	with open(merge_file_path, 'wb+') as merge_data:
		for chunk in merge_file.chunks():
			merge_data.write(chunk)
		merge_data.close()
	return merge_file_path

def send_status_email(model_name, email_to):
	global df
	status_file_name = 'Merge_' + model_name + '_Status' + '.xlsx'
	status_file_path = MEDIA_ROOT + "\\loop\\merge_entity\\" + status_file_name
	excel_writer = pd.ExcelWriter(status_file_path)
	df.to_excel(excel_writer = excel_writer, sheet_name = 'Sheet1', index = False)
	excel_writer.save()

	email = EmailMessage()
	email.subject = "Status mail"
	email.body = "PFA the status of merge request"
	email.from_email = EMAIL_HOST_USER
	email.to = [email_to]
	email.attach_file(status_file_path)
	email.send()
	os.remove(status_file_path)

def update_records(related_models, old, new):
	print "trying update"

	for related_model in related_models:
		related_model_column = related_models[related_model]
		related_model_obj = get_model('loop', related_model)

		kwargs_old = {related_model_column: old}
		kwargs_new = {related_model_column: new}


		related_model_obj.objects.filter(**kwargs_old).update(**kwargs_new)

		print "updated", related_model, related_model_column 

def delete_entity(model,model_name, record):
	print record
	kwargs = {cnf.models[model_name]['col_name']: record}
	instance = model.objects.get(**kwargs)
	instance.delete()

	print "deleted", model_name, record

def merge_bodies(model_name, index, row):
	print "merging row"
	global df
	initial = row['Initial ID']
	final = row['Final ID']

	kwargs = {cnf.models[model_name]['col_name']: final}

	model = get_model('loop', model_name)

	try:
		with transaction.atomic():
			print "trying merge"
			final_obj = model.objects.get(**kwargs)
			update_records(cnf.models[model_name]['dependencies'], initial, final)
			delete_entity(model, model_name, initial)

			df.set_value(index, 'Status', 'Pass')
			print index, "success", df
	except:
		df.set_value(index, 'Status', 'Fail')
		print index, "failed", df

def merge(model, merge_file_path, email_to):
	global df
	df = pd.DataFrame()
	df = pd.read_excel(merge_file_path, sheetname=0)

	#Add status column for merge request
	num_of_rows = len(df['Initial ID'])
	status = [None] * num_of_rows
	df['Status'] = pd.Series(status).values

	common_ids = set(df['Initial ID']) & set(df['Final ID'])

	for i, row in df.iterrows():
		if(row['Initial ID'] in common_ids or row['Final ID'] in common_ids):
			df.set_value(i, 'Status', 'Fail')
		else:
			pass
			merge_bodies(model, i, row)

	send_status_email(model, email_to)
	