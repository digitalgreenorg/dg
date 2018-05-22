# -*- coding: utf-8 -*-

import json
import xlsxwriter
from io import BytesIO
import re

#from weasyprint import HTML

from config import *
from django.template.loader import render_to_string
#from dg.settings import LOCALE
#import locale as lc


TOTAL_NUMBER_OF_PRINTABLE_COLUMNS = 10
NAME_OF_SHEETS = ['Aggregator', 'Commission Agent', 'Transporter']
CELL_ROW_VALUE = 2

def write_heading_in_sheet(ws_obj, heading_str, format_str):
    ws_obj.set_column('A:L', 10)
    ws_obj.merge_range('A1:L1', heading_str, format_str)
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


def write_headers_for_sheet(ws_obj, row_index, col_index, label, column_width, format_str):
    """
    Writes headers in the Excel sheets
    """
    col_width = column_width if column_width else DEFAULT_COLUMN_WIDTH
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
                                        column_width=col.get('column_width'),
                                        format_str=bold)
                cell_value = [CELL_ROW_VALUE, col_index]
                if col.get('total') is not None and col.get('total') != False:
                    total_value_in_column.append(int(col_index))
                if col.get('formula') is not None:
                    column_formula_list.append({'formula': col.get('formula'),
                                                'col_index': col_index})
            except Exception as e:
                pass
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
    formatted_post_data = prepare_value_data_generic(request.body)
    return formatted_post_data


def get_combined_data_and_sheets_formats(formatted_post_data):
    excel_output = BytesIO()
    workbook = xlsxwriter.Workbook(excel_output)
    # selecting a general font
    heading_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 9,
                                                       'text_wrap': True})
    header_format = set_format_for_heading(workbook=workbook,
                                           format_str={'bold':1, 'font_size': 9,
                                                       'text_wrap': True})
    row_format = set_format_for_heading(workbook=workbook,
                                        format_str=formatted_post_data.get('cell_format'))
    total_cell_format = set_format_for_heading(workbook=workbook,
                                              format_str={'bold':1,
                                                          'font_size': 9,
                                                          'num_format':'#,##0.00',
                                                          'align':'right',
                                                          'text_wrap': True})
    name_of_sheets = formatted_post_data.get('name_of_sheets')
    combined_data = formatted_post_data.get('combined_data')
    heading_of_sheets = formatted_post_data.get('heading_of_sheets')
    combined_header = formatted_post_data.get('combined_header')
    sheet_header = formatted_post_data.get('sheet_header')
    sheet_footer = formatted_post_data.get('sheet_footer')
    data_dict = {'name_of_sheets': name_of_sheets, 'combined_data': combined_data, 'combined_header': combined_header,
                 'heading_of_sheets': heading_of_sheets, 'workbook': workbook, 'heading_format': heading_format,
                 'header_format': header_format, 'row_format': row_format,
                 'total_cell_format': total_cell_format, 'sheet_header': sheet_header, 'sheet_footer': sheet_footer,
                 'excel_output': excel_output}
    return data_dict


def excel_processing(workbook, name_of_sheets, heading_of_sheets, heading_format, row_format, total_cell_format, header_format, combined_data,
                        combined_header, sheet_header, sheet_footer):
    # for developing exceptions
    try:
        for sheet_index, item in enumerate(name_of_sheets):
            ws = workbook.add_worksheet(name_of_sheets[sheet_index])
            ws.set_margins(0.1, 0.1)
            # setting the col width
            write_heading_in_sheet(ws_obj=ws,
                                   heading_str=heading_of_sheets[sheet_index],
                                   format_str=heading_format)
            # getting the cell value so that we will write values of columns
            write_header_in_excel = ws.set_header('&C'+sheet_header if sheet_header is not None else '')
            cell_value_from_headers = \
                get_headers_from_template_dict(ws, sheet_index, combined_header, header_format)
            write_footer_in_excel = ws.set_footer('&C'+sheet_footer if sheet_footer is not None else '')
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

            #Add comment in Aggregator sheet
            if(sheet_index==0):
                comment_row=str(write_values.get('end') + 3)
                ws.merge_range('A'+comment_row+':L'+comment_row, "**Quantity is deducted for farmers having incorrect/unavailable mobile numbers.", row_format)
                ap_formula_row = write_values.get('end') + 4
                ws.merge_range('A'+str(ap_formula_row)+':D'+str(ap_formula_row), "##AP calculation formula (Bihar)", row_format)
                ws.merge_range('E'+str(ap_formula_row)+':L'+str(ap_formula_row), " = 0.2*Q ; Q<=2000", row_format)
                ws.merge_range('E'+str(ap_formula_row+1)+':L'+str(ap_formula_row+1), " = 0.2*2000 + 0.1*(Q-2000) ; Q>2000", row_format)
                ws.merge_range('A'+str(ap_formula_row+2)+':D'+str(ap_formula_row+2), "##AP calculation formula (Maharashtra)", row_format)
                ws.merge_range('E'+str(ap_formula_row+2)+':L'+str(ap_formula_row+2), " = 0.25*Q", row_format)
                ws.merge_range('A'+str(ap_formula_row+3)+':D'+str(ap_formula_row+3), "##AP calculation formula (Bangladesh)", row_format)
                ws.merge_range('E'+str(ap_formula_row+3)+':L'+str(ap_formula_row+3), " = 0.5*Q", row_format)

    except Exception as e:
        pass
    return workbook


def prepare_value_data_generic(data):
    if isinstance(data,str):
        data = json.loads(data)
    combined_data = []
    combined_header = {}
    name_of_sheets = []
    heading_of_sheets = []
    combined_header = data.get('header')
    data_dict = data.get('data')
    cell_format = data.get('cell_format')
    sheet_header = data.get('sheet_header')
    sheet_footer = data.get('sheet_footer')

    for sheet_index, sheet in enumerate(data_dict.keys()):
        sheet_data = data_dict.get(sheet).get('data')
        combined_data.append(sheet_data)
        if data_dict.get(sheet).get('sheet_name') is None or data_dict.get(sheet).get('sheet_name') == '' :
            name_of_sheets.append('Sheet '+str(sheet_index + 1))
        else:
            name_of_sheets.append(data_dict.get(sheet).get('sheet_name'))

        if data_dict.get(sheet).get('sheet_heading') is None:
            heading_of_sheets.append('')
        else:
            heading_of_sheets.append(data_dict.get(sheet).get('sheet_heading'))

    combined_dict = {'combined_data': combined_data, 'combined_header': combined_header, 'name_of_sheets' : name_of_sheets,
                        'heading_of_sheets': heading_of_sheets, 'cell_format': cell_format,
                        'sheet_header': sheet_header, 'sheet_footer': sheet_footer}

    return combined_dict


# this function requires installation of WeasyPrint for generating PDF file.
# Dependencies- Pango, GdkPixbuf, and cairo can not be installed with pip and
# need to be installed from your platform’s packages. use the following command
# for Ubuntu
# sudo apt-get install build-essential python-dev python-pip python-cffi libcairo2 libpango1.0-0 libpangocairo-1.0.0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
#
# for Mac:
# brew install pkg-config libffi
# PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig pip install cffi
def generate_pdf(pdf_output, data_dict):
    try:
        lc.setlocale(lc.LC_ALL, LOCALE)
        table_data = get_table_data(data_dict)
        html_template = render_to_string('app_dashboards/payment_pdf.html', {'header': data_dict.get('sheet_header'), 'footer': data_dict.get('sheet_footer'), 'values': table_data})
        HTML(string=html_template).write_pdf(pdf_output)
        pdf = pdf_output.getvalue()
        pdf_output.close()
        return pdf
    except Exception as e:
        pass


def get_table_data(data_dict):
    try:
        name_of_sheets = data_dict.get('name_of_sheets')
        heading_of_sheets = data_dict.get('heading_of_sheets')
        combined_data = data_dict.get('combined_data')
        combined_header = data_dict.get('combined_header')

        table_data_final = []

        for sheet_index, item in enumerate(name_of_sheets):
            table_data = []
            data = {}
            comments = []
            headers = combined_header.values()[sheet_index]

            # append data for header and calculate column widths
            for header_index, header_value in enumerate(headers):
                header_value['column_width'] = header_value.get('column_width') * 6.3
                header_value['align'] = 'center'
            data['heading_of_sheet'] = heading_of_sheets[sheet_index]
            data['headers'] = headers
            if len(combined_data[sheet_index]) > 0:
                total_vals = [0] * len(combined_data[sheet_index][0])
                total_vals_str = []
                for value_list in combined_data[sheet_index]:
                    value_data = []
                    for i, value in enumerate(value_list):
                        if type(value) is int or type(value) is float:
                            value_data.append(lc.format('%.2f', value, grouping=True))
                            if headers[i].get('total'):
                                total_vals[i] += value
                            headers[i]['align'] = 'right'
                        elif value is None:
                            value_data.append("")
                        else:
                            value_data.append(value)
                    table_data.append(value_data)

                for i, value in enumerate(total_vals):
                    if headers[i].get('total'):
                        total_vals_str.append(lc.format('%.2f', value, grouping=True))
                        #total_vals_str.append(u"{:,.2f}".format(value))
                    else:
                        total_vals_str.append("")
                table_data.append(total_vals_str)
            data['data'] = table_data

            # Add comment in Aggregator part
            if sheet_index == 0:
                comments.append("     **Quantity is deducted for farmers having incorrect/unavailable mobile numbers.")
                comments.append("     ##AP calculation formula (Bihar)              = 0.2*Q ; Q<=2000")
                comments.append("                                                   = 0.2*2000 + 0.1*(Q-2000) ; Q>2000")
                comments.append("     ##AP calculation formula (Maharashtra)        = 0.25*Q")
                comments.append("     ##AP calculation formula (Bangladesh)         = 0.5*Q")
            data['comments'] = comments
            table_data_final.append(data)

        return table_data_final
    except Exception as e:
        pass

