import csv
import time
import datetime
import pandas as pd

from django.db.models import get_model
from dg.settings import MEDIA_ROOT
from pytz import timezone

from loop.models import Farmer, CombinedTransaction
from loop import mergeentityconfig as cnf

def save_file(merge_file):
	merge_file_name = "MergeEntities_" + str(datetime.datetime.now(timezone('Asia/Kolkata')).strftime('%Y_%m_%d_%H_%M_%S_%f')) + '.csv'
	merge_file_path =  MEDIA_ROOT + "\\loop\\merge_entity\\" + merge_file_name
	with open(merge_file_path, 'wb+') as merge_data:
		for chunk in merge_file.chunks():
			merge_data.write(chunk)
		merge_data.close()
	return merge_file_path

def update_records(related_models, old, new):

	for related_model in related_models:
		related_model_column = related_models[related_model]
		related_model_obj = get_model('loop', related_model)

		kwargs_old = {related_model_column: old}
		kwargs_new = {related_model_column: new}


		related_model_obj.objects.filter(**kwargs_old).update(**kwargs_new)

		print "updated", related_model, related_model_column 

def  delete_entity(model,model_name, record):
	print record
	kwargs = {cnf.models[model_name][0]: record}
	instance = model.objects.get(**kwargs)
	instance.delete()

	print "deleted", model_name, record

def merge_bodies(model, row):
	model_name = model
	initial = row['Initial ID']
	final = row['Final ID']

	kwargs = {cnf.models[model_name][0]: final}

	model = get_model('loop', model_name)
	final_obj = model.objects.get(**kwargs)

	update_records(cnf.models[model_name][1], initial, final)
	delete_entity(model, model_name, initial)

def merge(model, merge_file_path):
	col_names = ['Initial ID', 'Final ID']
	df = pd.read_csv(merge_file_path, usecols = col_names)
	for index, row in df.iterrows():
		merge_bodies(model, row)