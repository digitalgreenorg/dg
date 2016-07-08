import xlrd
import urllib2
from datetime import datetime 
from django.core.management.base import BaseCommand
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *


class Command(BaseCommand):

    def read_data(self,path):
        sheet_index = 0
        starting_row = 2
        data = {}
        open_file = xlrd.open_workbook(path)
        sheet = open_file.sheet_by_index(sheet_index)
        total_rows = sheet.nrows
        row = starting_row
        while row<total_rows:
            column = 0
            if sheet.cell(row,column).value != '':
                category = sheet.cell(row,column).value
                if category not in data:
                    data[category] = {}
                column = column + 1
                while row<total_rows and ((sheet.cell(row,column-1).value==category) or  (sheet.cell(row,column-1).value == '')):
                    sub_column = column
                    if sheet.cell(row,sub_column).value != '':
                        sub_category = sheet.cell(row,sub_column).value
                    else:
                        row += 1
                        continue
                    if sub_category not in data[category]:
                        data[category][sub_category] = []
                    sub_column += 1
                    while row<total_rows and (sheet.cell(row,sub_column-1).value==sub_category or  sheet.cell(row,sub_column-1).value == ''):
                        practice_column = sub_column
                        if sheet.cell(row,practice_column).value != '':
                            practice = sheet.cell(row,practice_column).value
                            data[category][sub_category].append(practice)
                        row += 1
            else:
                row += 1
        for category in data:
            temp = []
            for sub_category in data[category]:
                temp += data[category][sub_category]
            for sub_category in data[category]:
                data[category][sub_category] = temp
        return data


    def handle(self, *args, **options):

        file_path = "practice_mapping.xlsx"
        #read data from file
        data = self.read_data(file_path)
        #Write data in database
        log_file = "category_sub_category_topic_entry_duplicate_error_log"
        logs = "\nName : Value : Exception"
        for category in data:
            try:
                cat_obj = Category.objects.get(category_name = category)
            except Category.DoesNotExist as e:
                logs += "Category: " + category + " : " + str(e) + "\n"
                cat_obj = Category(category_name = category)
                cat_obj.save()
            for sub_category in data[category]:
                try:
                    sub_cat_obj = SubCategory.objects.get(subcategory_name=sub_category,category__category_name=category)
                except SubCategory.DoesNotExist as e:
                    logs += "SubCategory: " + sub_category + " : " + str(e) + "\n"
                    sub_cat_obj = SubCategory(subcategory_name=sub_category,category=cat_obj)
                    sub_cat_obj.save()
                for practice in data[category][sub_category]:
                    try:
                        practice_obj = VideoPractice.objects.get(videopractice_name=practice,subcategory__subcategory_name=sub_category)
                    except VideoPractice.DoesNotExist as e:
                        print e
                        logs += "VideoPractice: " + practice + " : " + str(e) + "\n"
                        practice_obj = VideoPractice(videopractice_name=practice,subcategory=sub_cat_obj)
                        practice_obj.save()

        with open(log_file,"w") as log:
            log.write(logs)