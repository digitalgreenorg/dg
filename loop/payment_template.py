# Create your views here.
import json
import xlsxwriter
from django.http import JsonResponse
from io import BytesIO
import re

from config import *
from django.http import HttpResponse

TOTAL_NUMBER_OF_PRINTABLE_COLUMNS = 10
NAME_OF_SHEETS = ['Aggregator', 'Commission Agent', 'Transporter']
CELL_ROW_VALUE = 2

def write_heading_in_sheet(ws_obj, heading_str, format_str):
    ws_obj.set_column('A:F', 10)
    ws_obj.merge_range('A1:F1', heading_str, format_str)
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


def write_headers_for_sheet(ws_obj, row_index, col_index, label, coloumn_width, format_str):
    """
    Writes headers in the Excel sheets
    """
    col_width = coloumn_width if coloumn_width else DEFAULT_COLUMN_WIDTH
    ws_obj.set_column(col_index, col_index, col_width)
    ws_obj.write(row_index, col_index, label, format_str)
    return


def get_headers_from_template_dict(ws_obj, sheet_index, header_dict, bold):
    """
    Fetch Headers from Variable Dict in the Excel sheets
    """
    cell_value = None
    column_formula_list = []
    total_value_in_column = []
    header_dict = header_dict
    for col_index, col in enumerate(header_dict.values()[sheet_index]):
        if not isinstance(col, list):
            try:
                write_headers_for_sheet(ws_obj=ws_obj,
                                        row_index=CELL_ROW_VALUE,
                                        col_index=col_index,
                                        label=col.get('label'),
                                        coloumn_width=col.get('coloumn_width'),
                                        format_str=bold)
                cell_value = [CELL_ROW_VALUE, col_index]
                if col.get('total') != False:
                    total_value_in_column.append(int(col_index))
                if col.get('formula') is not None:
                    column_formula_list.append({'formula': col.get('formula'),
                                                'col_index': col_index})
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
        ws_obj.write(end, item, '=SUM('+chr(item + 65)+str(start)+':'+chr(item + 65)+str(end)+')', format_str)
    return

def format_web_request(request):
    formatted_post_data = prepare_value_data(request.body)
    return formatted_post_data


def get_combined_data_and_sheets_formats(formatted_post_data):
    excel_output = BytesIO()
    workbook = xlsxwriter.Workbook(excel_output)
    # selecting a general font
    heading_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 9,
                                                       'text_wrap': True})
    header_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 10,
                                                       'text_wrap': True})
    row_format = set_format_for_heading(workbook=workbook,
                                        format_str={'bold':0, 'font_size': 10,
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
                 'workbook': workbook, 'heading_format': heading_format,
                 'header_format': header_format, 'row_format': row_format,
                 'total_cell_format': total_cell_format, 
                 'excel_output': excel_output}
    return data_dict


def excel_processing(workbook, name_of_sheets, heading_format, row_format, total_cell_format, header_format, combined_data):
    # for developing exceptions
    try:
        for sheet_index, item in enumerate(name_of_sheets):
            ws = workbook.add_worksheet(NAME_OF_SHEETS[sheet_index])
            # setting the col width
            write_heading_in_sheet(ws_obj=ws,
                                   heading_str=name_of_sheets[sheet_index],
                                   format_str=heading_format)
            # getting the cell value so that we will write values of columns
            write_header_in_excel = ws.set_header(HEADER_STRING)
            cell_value_from_headers = \
                get_headers_from_template_dict(ws, sheet_index, header_dict, header_format)
            write_footer_in_excel = ws.set_footer(FOOTER_STRING)
            # finally writing in process
            write_values = \
                write_values_to_sheet(ws, combined_data[sheet_index], cell_value_from_headers.get('cell_value'), row_format)
            write_total_in_excel_sheet(ws, write_values.get('start'),
                                       write_values.get('end'),
                                       cell_value_from_headers.get('formulacolumn_dict'),
                                       total_cell_format)
            write_formula_in_values(ws,
                                    combined_data[sheet_index],
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
    aggregator_data = data.get('aggregator_data')
    commission_data = data.get('gaddidar_data')
    transport_data = data.get('transporter_data')

    sheet1_file_name = u''+aggregator_data.get('name')
    sheet2_file_name = u''+commission_data.get('name')
    sheet3_file_name = u''+transport_data.get('name')

    aggregator_data = aggregator_data.get('data')
    commission_data = commission_data.get('data')
    transport_data = transport_data.get('data')

    name_of_sheets=[sheet1_file_name, sheet2_file_name, sheet3_file_name]
    combined_data = [aggregator_data, commission_data, transport_data]
    combined_dict =  {'combined_data': combined_data,
                      'name_of_sheets': name_of_sheets}
    return combined_dict


