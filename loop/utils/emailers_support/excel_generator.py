__author__ = 'Lokesh'

import xlsxwriter

# This dictionary should contain all formats that we want to use.
format = {'date_format': {'num_format': 'd mmm yyyy'}}

# Creates a workbook
def create_workbook(workbook_name):
    workbook = xlsxwriter.Workbook(workbook_name)
    return workbook

# Creates all formats in the workbook
def create_format(list_of_format, workbook):
    formats_created = {}
    for formats in list_of_format:
        formats_created[formats] = workbook.add_format(format[formats])
    return formats_created

# Purpose: Takes a xlsx file as parameter and enters data in it
# Parameters: workbook - name of xlsx file e.g. 'xyz.xlsx'
#             sheets_data - dictionary with key = sheet name and value = list of list of sheets data e.g. {'Dev': [[1,2],[3,4]]}
#             table_properties - dictionary with properties of xlsx writer. No default properties right now. Keep Data field - None.
#             table_position - contains row, col of first cell of table e.g. {'row': 0, 'col': 0}
#             column_width_and_format - Dictionary of all column widths. {'A:A': 9.5}
#             sheet name should be string

default_table_position = {'row': 0, 'col': 0}
def create_xlsx(workbook, sheets_data, table_properties, table_position = default_table_position, column_width_and_format = None):
    sheet_name = {}
    for keys in sheets_data.keys():
        rows_count = len(sheets_data[keys])
        columns_count = len(sheets_data[keys][0]) - 1
        sheet_name[keys] = workbook.add_worksheet(keys)
        row_position = table_position['row']
        col_position = table_position['col']
        table_properties['data'] = sheets_data[keys]
        sheet_name[keys].add_table(row_position, col_position, rows_count, columns_count, table_properties)
        for keys1 in column_width_and_format.keys():
            sheet_name[keys].set_column(keys1, column_width_and_format[keys1])

    workbook.close()