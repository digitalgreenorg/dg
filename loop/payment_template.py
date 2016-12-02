# Create your views here.
import json
import xlsxwriter
from django.http import JsonResponse
from io import BytesIO
import re

from config import *
from django.http import HttpResponse

TOTAL_NUMBER_OF_PRINTABLE_COLUMNS = 10
NUMBER_OF_SHEETS = 3
NAME_OF_SHEETS = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4']
CELL_ROW_VALUE = 2

def write_heading_in_sheet(ws_obj, heading_str, format_str):
    ws_obj.set_column('A:H', 200)
    ws_obj.merge_range('A1:H1', heading_str, format_str)
    # ws_obj.write('A1', heading_str, format_str)
    return ws_obj


def set_format_for_heading(workbook, format_str):
    """
    Format string for heading
    """
    final_format = workbook.add_format(format_str)
    return final_format

def align_col_row_width_for_heading(ws_obj, row_number, merge_col_width, merge_row_width):
    """
    Alignment us for rows and columns
    """
    ws_obj.set_column('B:G', merge_col_width)
    ws_obj.set_row(row_number, merge_row_width)
    return ws_obj

def merge_column_in_excel(ws_obj, first_cell, second_cell, heading, format_str):
    """
    Merge Columns for increase in heading
    """
    ws_obj.merge_range(first_cell+':'+second_cell, heading ,format_str)
    return ws_obj


def write_headers_for_sheet(ws_obj, row_index, col_index, label, format_str):
    """
    Writes headers in the Excel sheets
    """
    ws_obj.set_column(col_index, col_index, 9)
    ws_obj.write(row_index, col_index, label, format_str)
    return


def get_headers_from_template_dict(ws_obj, idx, header_dict, bold):
    """
    Fetch Headers from Variable Dict in the Excel sheets
    """
    cell_value = None
    column_formula_list = []
    total_value_in_column = []
    header_dict = header_dict
    for item in header_dict.values():
        for i in item[idx].values():
            for k in i.values():
                for c, j in enumerate(k):
                    if not isinstance(j, list):
                        try:
                            write_headers_for_sheet(ws_obj=ws_obj,
                                                    row_index=CELL_ROW_VALUE,
                                                    col_index=c,
                                                    label=j.get('label'), format_str=bold)
                            cell_value = [CELL_ROW_VALUE, c]
                            if j.get('total') != False:
                                total_value_in_column.append(c)
                            if j.get('formula') is not None:
                                column_formula_list.append({'formula': j.get('formula'),
                                                            'col_index': c})
                        except Exception as e:
                            print e
    data_dict = {'cell_value': cell_value, 'formulacolumn_dict': total_value_in_column,
                 'formula_list': column_formula_list}
    return data_dict

def write_values_to_sheet(ws_obj, sheet_data_list, cell_value, format_str):
    """
    Write Values to sheets
    """
    row = cell_value[0] + 1
    for i in range(0,len(sheet_data_list)):
        col = 0
        for j in range(0,len(sheet_data_list[0])):
            ws_obj.write(row, col, sheet_data_list[i][j], format_str)
            col += 1
        row += 1
    start = cell_value[0] + 2
    end = start + len(sheet_data_list) - 1
    data_dict = {'start': start, 'end': end}
    return data_dict


def read_formula_and_write_to_excel(ws_obj, formula, start, end, format_str):
    col_index = chr(formula.get('col_index') + 65)
    actual_formula = formula.get('formula')
    final_str = '='
    i = 0
    iter_formula = actual_formula.split()
    while i < len(iter_formula):
        #regex matching
        if re.match('[a-zA-Z]+', iter_formula[i]) is not None:
            final_str += iter_formula[i] + str(start)
        else:
            final_str += iter_formula[i]    
        i += 1
    ws_obj.write(col_index+str(start) , final_str, format_str)
    return


def write_formula_in_values(ws_obj, sheet_data_list, cell_value, formula_list, format_str):
    # write the forumla in cell
    start = cell_value[0] + 2
    end = start + len(sheet_data_list) - 1
    temp_start = start
    for item in formula_list:
        start = temp_start
        while start <= end:
            read_formula_and_write_to_excel(ws_obj, item, start, end, format_str)
            start += 1
    return

def write_total_in_excel_sheet(ws_obj, start, end, formulacolumn_dict, format_str):
    for item in formulacolumn_dict:
        ws_obj.write(end+2, item, '=SUM('+chr(item + 65)+str(start)+':'+chr(item + 65)+str(end)+')', format_str)
    return

def format_web_request(request):
    formatted_post_data = prepare_value_data(request.body)
    return formatted_post_data


def get_combined_data_and_sheets_formats(formatted_post_data):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    # selecting a general font
    heading_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 15,
                                                       # 'align': 'center',
                                                       'text_wrap': False})
    header_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 10,
                                                       'text_wrap': True})
    row_format = set_format_for_heading(workbook=workbook,
                                        format_str={'bold':0, 'font_size': 10,
                                                    # 'align': 'left',
                                                    'num_format':'#,##0.00',
                                                    'text_wrap': True})
    total_cell_format = set_format_for_heading(workbook=workbook,
                                              format_str={'bold':1, 
                                                          'font_size': 10,
                                                          'num_format':'#,##0.00',
                                                          'align':'right',
                                                          'text_wrap': True})
    name_of_sheets = formatted_post_data.get('name_of_sheets')
    combined_data = formatted_post_data.get('combined_data')
    data_dict = {'name_of_sheets': name_of_sheets, 'combined_data': combined_data,
                 'workbook': workbook, 'header_format': header_format,
                 'header_format': header_format, 'row_format': row_format,
                 'total_cell_format': total_cell_format, 
                 'output': output}
    return data_dict


def excel_processing(workbook, name_of_sheets, heading_format, row_format, total_cell_format, header_format, combined_data):
    # for developing exceptions
    try:
        for idx, item in enumerate(name_of_sheets):
            ws = workbook.add_worksheet('Sheet'+ str(idx+1))
            # setting the col width
            write_heading_in_sheet(ws_obj=ws,
                                   heading_str=name_of_sheets[idx],
                                   format_str=heading_format)
            # getting the cell value so that we will write values of columns
            cell_value_from_headers = \
                get_headers_from_template_dict(ws, idx, header_dict, header_format)
            # finally writing in process
            write_values = \
                write_values_to_sheet(ws, combined_data[idx], cell_value_from_headers.get('cell_value'), row_format)
            write_total_in_excel_sheet(ws, write_values.get('start'),
                                       write_values.get('end'),
                                       cell_value_from_headers.get('formulacolumn_dict'),
                                       total_cell_format)
            write_formula_in_values(ws,
                                    combined_data[idx],
                                    cell_value_from_headers.get('cell_value'),
                                    cell_value_from_headers.get('formula_list'),
                                    row_format)
            
    except Exception as e:
        print e
    return workbook

def prepare_value_data(data):
    """
    Process the post data request and breaking into individual sheet data
    """
    data = json.loads(data)
    aggregator_data = data[0]
    commission_data = data[1]
    transport_data = data[2]
    sheet1_file_name = u''+aggregator_data[-1][0]
    sheet2_file_name = u''+commission_data[-1][0]
    sheet3_file_name = u''+transport_data[-1][0]
    aggregator_data = aggregator_data[:len(aggregator_data)-1]
    commission_data = commission_data[:len(commission_data)-1]
    transport_data = transport_data[:len(transport_data)-1]
    name_of_sheets=[sheet1_file_name, sheet2_file_name, sheet3_file_name]
    combined_data = [aggregator_data, commission_data, transport_data]
    combined_dict =  {'combined_data': combined_data,
                      'name_of_sheets': name_of_sheets}
    return combined_dict


