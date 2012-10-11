from dg import settings
from django.core.management import setup_environ
setup_environ(settings)
from dashboard.models import *
import xlrd

def get_video_schedule():
    book = xlrd.open_workbook("video_schedule.xls", formatting_info=1)
    sheets = book.sheet_names()
    sheet = book.sheet_by_index(0)   # using the first sheet
    dates = ['2012-01-01','2012-01-16','2012-02-01','2012-02-16','2012-03-01','2012-03-16','2012-04-01','2012-04-16','2012-05-01','2012-05-16','2012-06-01','2012-06-16',
             '2012-07-01','2012-07-16','2012-08-01','2012-08-16','2012-09-01','2012-09-16','2012-10-01','2012-10-16','2012-11-01','2012-11-16','2012-12-01','2012-12-16','2012-12-31']
    
    row = 2
    vid_dict = []
    while( row < sheet.nrows):
        col = 0    
        vid_id = Video.objects.filter(title = sheet.cell(row, col).value).values_list('id', flat = True)
        col += 1
        if len(vid_id) == 1 :
            while( col < sheet.ncols ):
                format_info = sheet.cell_xf_index(row, col)
                format_info = book.xf_list[format_info]
                bg_color = format_info.background.pattern_colour_index
                if bg_color == 13:
                    low = col
                    while( col < sheet.ncols):
                        format_info = sheet.cell_xf_index(row, col)
                        format_info = book.xf_list[format_info]
                        bg_color = format_info.background.pattern_colour_index
                        if bg_color == 13:
                            col += 1
                        else:
                            high = col
                            vid_dict.append({'id': vid_id[0],
                                            'low_val': dates[low-2],
                                            'high_val': dates[high-2] })
                            break                  
                col += 1 
        row += 1
    
    return vid_dict 