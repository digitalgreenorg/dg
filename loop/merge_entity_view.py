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

from loop.models import Farmer, CombinedTransaction, Gaddidar, GaddidarCommission, GaddidarShareOutliers, CropLanguage
from loop_ivr.models import PriceInfoLog
from loop.configs import mergeentityconfig as merge_cnf

def save_file(merge_file):
	merge_file_name = "MergeEntities_" + str(datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y_%m_%d_%H_%M_%S_%f')) + '.xlsx'
	merge_file_path =  MEDIA_ROOT + "\\loop\\merge_entity\\" + merge_file_name
	with open(merge_file_path, 'wb+') as merge_data:
		for chunk in merge_file.chunks():
			merge_data.write(chunk)
		merge_data.close()
	return merge_file_path

def send_status_email(df, model_name, email_to):
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
	for related_model in related_models:
		related_model_column = related_models[related_model]['column']
		related_model_obj = get_model(related_models[related_model]['app'], related_model)

		kwargs_old = {related_model_column: old}
		kwargs_new = {related_model_column: new}

		related_model_obj.objects.filter(**kwargs_old).update(**kwargs_new)

def delete_entity(model,model_name, record):
	kwargs = {merge_cnf.models[model_name]['col_name']: record}
	instance = model.objects.get(**kwargs)
	instance.delete()

def check_crop_language(language, crops):
	crop_lang = CropLanguage.objects.filter(crop_id__in=crops)
	dict_lang_wise_names = {}
	for entry in crop_lang:
		if (entry.language_id not in dict_lang_wise_names.keys()):
			dict_lang_wise_names[entry.language_id] = set()
		dict_lang_wise_names[entry.language_id].add(entry.crop_name)
	for lang in dict_lang_wise_names:
		if lang != language and len(dict_lang_wise_names[lang]) > 1:
			return False, None
	return True, crop_lang

def merge_bodies(df, model_name, index, initial, final):

	kwargs = {merge_cnf.models[model_name]['col_name']: final}

	model = get_model('loop', model_name)

	try:
		with transaction.atomic():
			update_records(merge_cnf.models[model_name]['dependencies'], initial, final)
			delete_entity(model, model_name, initial)

			df.set_value(index, 'Status', 'Pass')
	except Exception as e:
		df.set_value(index, 'Status', 'Fail')
		df.set_value(index, 'Exception', str(e))

def merge(model, merge_file_path, email_to):
	df = pd.read_excel(merge_file_path, sheet_name=0)	
	common_ids = set(df['Initial ID']) & set(df['Final ID'])
	ids = ', '.join(str(e) for e in common_ids)
	duplicate_initial_id = df.duplicated(['Initial ID'], keep=False)	

	for i, row in df.iterrows():
		if(row['Initial ID'] in common_ids or row['Final ID'] in common_ids):
			df.set_value(i, 'Status', 'Fail')
			df.set_value(i, 'Exception', 'IDs:['+ids+'] are presesnt in Final ID column too')
			continue
		if(duplicate_initial_id[i] == True):
			df.set_value(i, 'Status', 'Fail')
			df.set_value(i, 'Exception', 'Initial ID being changed multiple times')
			continue
		if model == 'Crop':
			crop_lang = CropLanguage.objects.filter(id__in=[row['Initial ID'], row['Final ID']]).values('crop_id', 'language_id')
			languages = set()
			crops = []
			for data in crop_lang:
				crops.append(data['crop_id'])
				languages.add(data['language_id'])
			if len(languages) > 1:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', 'Merge requested for different languages')
				continue
			for lang in languages:
				break
			check, crop_lang_queryset = check_crop_language(lang, crops)
			if check == True:
				try:
					initial_crop_lang = crop_lang_queryset.get(id=row['Initial ID'])#.values_list('crop_id', flat=True)[0]
					initial_crop_id = initial_crop_lang.crop_id
					final_crop_lang = crop_lang_queryset.get(id=row['Final ID'])#.values_list('crop_id', flat=True)[0]				
					final_crop_id = final_crop_lang.crop_id
					
					with transaction.atomic():
						crop_lang_queryset.get(crop_id=initial_crop_id).delete()
						merge_bodies(df, model, i, initial_crop_id, final_crop_id)
				except Exception as e:
					df.set_value(i, 'Status', 'Fail')
					df.set_value(i, 'Exception', str(e))
			else:
				df.set_value(i, 'Status', 'Fail')
				df.set_value(i, 'Exception', 'There is a conflict in crop names for other languages')
		else:
			merge_bodies(df, model, i, row['Initial ID'], row['Final ID'])

	send_status_email(df, model, email_to)
	