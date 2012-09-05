import settings
from django.core.management import setup_environ
setup_environ(settings)
from dashboard.models import *
import xlrd

def get_video_schedule():
    book = xlrd.open_workbook("video_schedule.xls", formatting_info=1)
    sheets = book.sheet_names()
    sheet = book.sheet_by_index(0)   # using the first sheet
    dates = ['01-01-2012','16-01-2012','01-02-2012','16-02-2012','01-03-2012','16-03-2012','01-04-2012','16-04-2012',
             '01-05-2012','16-05-2012','01-06-2012','16-06-2012','01-07-2012','16-07-2012','01-08-2012','16-08-2012',
             '01-09-2012','16-09-2012','01-10-2012','16-10-2012','01-11-2012','16-11-2012','01-12-2012','16-12-2012',
             '31-12-2012']
    
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