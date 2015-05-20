import os

import xlrd

from django.core.management.base import BaseCommand

from libs.s3_utils import add_to_s3
from dg.settings import ACCESS_KEY, SECRET_KEY, MEDIA_ROOT, YOUTUBE_SIMPLE_ACCESS
from videos.models import Video
from videokheti.models import ActionType, Crop, Method, TimeYear, Video as videokheti_video, Title


class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = '''Creates initial cases for a new CommCare Application. Prerequisites:
    (1) Create project in CommCare.
    (2) Enter project information through admin.
    (3) Create atleast one CommCare user for this project.
    (4) Enter user, project and village permissions, through admin.
    '''

    def handle(self, *args, **options):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        workbook = xlrd.open_workbook(os.path.join(__location__, 'hindi_text.xlsx'))
        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            try:
                a = Crop.objects.get(name=worksheet.cell_value(curr_row, 1))
                print row
                a.hindi_text = worksheet.cell_value(curr_row, 2)
                a.save()
            except:
                pass
            try:
                a = TimeYear.objects.get(name=worksheet.cell_value(curr_row, 1))
                print row
                a.hindi_text = worksheet.cell_value(curr_row, 2)
                a.save()
            except:
                pass
            try:
                a = ActionType.objects.get(name=worksheet.cell_value(curr_row, 1))
                print row
                a.hindi_text = worksheet.cell_value(curr_row, 2)
                a.save()
            except:
                pass
            try:
                a = Method.objects.get(name=worksheet.cell_value(curr_row, 1))
                print row
                a.hindi_text = worksheet.cell_value(curr_row, 2)
                a.save()
            except:
                pass
            
        workbook = xlrd.open_workbook(os.path.join(__location__, 'hindi_title.xlsx'))
        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            #a = Video.objects.get(coco_video_id=worksheet.cell_value(curr_row, 0))
            try:
                a = videokheti_video.objects.get(coco_video_id=worksheet.cell_value(curr_row, 0))
                print row
                a.hindi_text = worksheet.cell_value(curr_row, 3)
                a.save()
            except:
                pass
 
        workbook = xlrd.open_workbook(os.path.join(__location__, 'Titles_Hindi.xlsx'))
        worksheet = workbook.sheet_by_name('Sheet1')
        num_rows = worksheet.nrows - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            #a = Video.objects.get(coco_video_id=worksheet.cell_value(curr_row, 0))
            try:
                a = Title(table=worksheet.cell_value(curr_row, 2),
                          title=worksheet.cell_value(curr_row, 0),
                          hindi_text=worksheet.cell_value(curr_row, 1))
                print row
                a.save()
            except Exception as e:
                print e