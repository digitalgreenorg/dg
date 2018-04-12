# -*- coding: utf-8 -*-

import json
import xlsxwriter
from django.http import JsonResponse
from io import BytesIO
import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from weasyprint import HTML

from config import *
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import RequestContext

import pandas as pd


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
        print e
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


class PdfPrint:
    def __init__(self, output):
        self.output = output
        self.pageSize = A4
        self.width, self.height = self.pageSize
        self.header = None
        self.footer = None

    def generate(self, data_dict, header, footer):
        try:
            doc = SimpleDocTemplate(self.output, rightMargin=50, leftMargin=50,
                                    topMargin=40, bottomMargin=50, pageSize=self.pageSize)

            # setting up styles
            styles = getSampleStyleSheet()
            cell_format = data_dict.get('cell_format')

            unicode_font = 'UnicodeFont'
            unicode_font_bold = 'UnicodeFontBold'

            self.header = header
            self.footer = footer

            # Font for displaying unicode characters,
            # currently this font contains glyphs for almost all indian languages
            pdfmetrics.registerFont(TTFont(unicode_font, 'NotoSans-Regular-Indian.ttf'))
            pdfmetrics.registerFont(TTFont(unicode_font_bold, 'NotoSans-Bold-Indian.ttf'))
            styles.add(ParagraphStyle(
                name="ParagraphTitle", fontSize=10, alignment=TA_JUSTIFY, fontName=unicode_font_bold))
            styles.add(ParagraphStyle(
                name="Justify", alignment=TA_JUSTIFY))
            styles.add(ParagraphStyle("Comment", fontSize=cell_format.get('font_size')))
            styles.add(ParagraphStyle("TableHeader", fontSize=8, alignment=TA_CENTER, fontName=unicode_font_bold))
            styles.add(ParagraphStyle("Text", fontSize=8, alignment=TA_CENTER, fontName=unicode_font))
            styles.add(ParagraphStyle("TextRight", fontSize=8, alignment=TA_RIGHT, fontName=unicode_font))
            styles.add(ParagraphStyle("TextBold", fontName=unicode_font_bold, fontSize=8, alignment=TA_CENTER))
            styles.add(ParagraphStyle("TextBoldRight", fontName=unicode_font_bold, fontSize=8, alignment=TA_RIGHT))
            styles.add(ParagraphStyle("CommentSpace", fontSize=cell_format.get('font_size'), leftIndent=179))

            # A list of complete data which goes in the pdf.
            pdfdata = list()
            pdfdata.append(Spacer(1, 12))

            name_of_sheets = data_dict.get('name_of_sheets')
            heading_of_sheets = data_dict.get('heading_of_sheets')
            combined_data = data_dict.get('combined_data')
            combined_header = data_dict.get('combined_header')

            for sheet_index, item in enumerate(name_of_sheets):
                table_data = []
                pdfdata.append(Paragraph(heading_of_sheets[sheet_index], styles['ParagraphTitle']))
                pdfdata.append(Spacer(1, 12))
                header_data = []
                col_widths = []
                headers = combined_header.values()[sheet_index]

                # append data for header and calculate column widths
                for header_index, header_value in enumerate(headers):
                    header_data.append(Paragraph(header_value.get('label'), styles['TableHeader']))
                    col_widths.append((header_value.get('column_width'))*6.3)
                table_data.append(header_data)
                total_vals = [0]*len(combined_data[sheet_index][0])
                total_vals_str = []
                for value_list in combined_data[sheet_index]:
                    value_data = []
                    for i, value in enumerate(value_list):
                        if type(value) is int or type(value) is float:
                            value_data.append(Paragraph(u"{0:.2f}".format(value), styles['TextRight']))
                            if headers[i].get('total'):
                                total_vals[i] += value
                        elif value is None:
                            value_data.append("")
                        else:
                            value_data.append(Paragraph(value, styles['Text']))
                    table_data.append(value_data)

                #manually calculate values for Total Payment (in Rs) (AP + TC - FC - CAC) for aggregator sheet
                if sheet_index == 0:
                    total_vals[8] = total_vals[4] + total_vals[5] - total_vals[6] - total_vals[7]
                for value in total_vals:
                    if value > 0:
                        total_vals_str.append(Paragraph(u"{0:.2f}".format(value), styles['TextBoldRight']))
                    else:
                        total_vals_str.append("")
                table_data.append(total_vals_str)

                # Create table
                data_table = Table(table_data, col_widths)
                data_table.hAlign = 'CENTER'
                data_table.setStyle(TableStyle(
                    [('INNERGRID', (0, 0), (-1, -1), 0, colors.black),
                     ('BOX', (0, 0), (-1, -1), 0, colors.black),
                     ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                     ('BACKGROUND', (0, 0), (-1, 0), colors.white)]
                ))

                pdfdata.append(data_table)
                pdfdata.append(Spacer(1, 30))

                # Add comment in Aggregator part
                if sheet_index == 0:
                    pdfdata.append(Paragraph("**Quantity is deducted for farmers having incorrect/unavailable mobile numbers.", styles['Comment']))

                    pdfdata.append(Spacer(1, 5))
                    pdfdata.append(Paragraph("##AP calculation formula (Bihar) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 0.2*Q ; Q<=2000", styles['Comment']))

                    pdfdata.append(Paragraph("= 0.2*2000 + 0.1*(Q-2000) ; Q>2000							", styles['CommentSpace']))
                    pdfdata.append(Paragraph("##AP calculation formula (Maharashtra) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 0.25*Q							", styles['Comment']))
                    pdfdata.append(Paragraph("##AP calculation formula (Bangladesh) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= 0.5*Q							", styles['Comment']))

                pdfdata.append(PageBreak())

            doc.multiBuild(pdfdata, onFirstPage=self.onMyPages, onLaterPages=self.onMyPages)
            pdf = self.output.getvalue()
            self.output.close()
            return pdf
        except Exception as e:
            print e

    def onMyPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 12)
        if self.header is not None:
            # draw header
            canvas.drawCentredString(self.width/2.0, self.height-30, self.header)

        if self.footer is not None:
            # draw footer
            canvas.drawCentredString(self.width/2.0, 30, self.footer)
        canvas.restoreState()


def printPDF(pdf_output, data_dict):
    try:
        table_data = getTableData(data_dict)
        html_template = render_to_string('app_dashboards/payment_pdf.html', {'header': data_dict.get('sheet_header'), 'footer': data_dict.get('sheet_footer'), 'values': table_data})

        HTML(string=html_template).write_pdf(pdf_output)
        pdf = pdf_output.getvalue()
        pdf_output.close()
        return pdf
    except Exception as e:
        print e


def getTableData(data_dict):
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
                print header_value['column_width']
            data['heading_of_sheet'] = heading_of_sheets[sheet_index]
            data['headers'] = headers
            if len(combined_data[sheet_index]) > 0:
                total_vals = [0] * len(combined_data[sheet_index][0])
                total_vals_str = []
                for value_list in combined_data[sheet_index]:
                    value_data = []
                    for i, value in enumerate(value_list):
                        if type(value) is int or type(value) is float:
                            value_data.append(u"{0:,.2f}".format(value))
                            if headers[i].get('total'):
                                total_vals[i] += value
                            headers[i]['align'] = 'right'
                        elif value is None:
                            value_data.append("")
                        else:
                            value_data.append(value)
                    table_data.append(value_data)

                # manually calculate values for Total Payment (in Rs) (AP + TC - FC - CAC) for aggregator sheet
                if sheet_index == 0:
                    total_vals[8] = total_vals[4] + total_vals[5] - total_vals[6] - total_vals[7]
                for value in total_vals:
                    if value > 0:
                        total_vals_str.append(u"{:,.2f}".format(value))
                    else:
                        total_vals_str.append("")
                table_data.append(total_vals_str)
            data['data'] = table_data

            # Add comment in Aggregator part
            if sheet_index == 0:
                comments.append("     **Quantity is deducted for farmers having incorrect/unavailable mobile numbers.")
                comments.append("     ##AP calculation formula (Bihar)                    = 0.2*Q ; Q<=2000")

                comments.append("                                                                          = 0.2*2000 + 0.1*(Q-2000) ; Q>2000							")
                comments.append("     ##AP calculation formula (Maharashtra)        = 0.25*Q")
                comments.append("     ##AP calculation formula (Bangladesh)         = 0.5*Q")
            data['comments'] = comments
            table_data_final.append(data)

        return table_data_final
    except Exception as e:
        print e

