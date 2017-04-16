__author__ = 'Lokesh'

import xlsxwriter
import pandas as pd


# This dictionary should contain all formats that we want to use.
format = {'date_format': {'num_format': 'd mmm yyyy'}, 'wrap_text': {'text_wrap': 1}}

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
def create_xlsx(workbook, sheets_data, table_properties, table_position = default_table_position, file_caption={}):
    sheet_name = {}

    for keys in sheets_data.keys():
        rows_count = len(sheets_data[keys])+2
        if len(sheets_data[keys]) > 0:
            columns_count = len(sheets_data[keys][0]) - 1
            sheet_name[keys] = workbook.add_worksheet(keys)
            # wr_format = workbook.add_format()
            # wr_format.set_text_wrap()
            row_position = table_position['row']
            col_position = table_position['col']
            table_properties['data'] = sheets_data[keys]
            sheet_name[keys].write('A1', file_caption[keys])
            format = workbook.add_format({'text_wrap': True})
            for elements in table_properties['columns']:
                sheet_name[keys].set_column(elements['col_seq'],elements['column_width'])
#                sheet_name[keys].set_text_wrap()

            sheet_name[keys].add_table(row_position, col_position, rows_count, columns_count, table_properties)
            for elements in table_properties['columns']:
                sheet_name[keys].write(elements['col_seq'][0]+'3', elements['header'],format)

    workbook.close()


# {(a, b, c): {d:e, f:g}}
def convert_query_result_in_nested_dictionary(query_result, keys_in_values, key_number):
    final_dictionary = {}
    for tuples in query_result:
        dict_value = []
        temp = ()
        if key_number == 0:
            return None
        if len(keys_in_values) > 0:  # To check whether inner dictionary needs to be provided keys separately
            for elements in keys_in_values:
                temp = ((elements, tuples[keys_in_values.index(elements) + key_number]),)
                dict_value += temp
            dict_value = dict(dict_value) # This is inner dictionary
            if key_number == 1:
                dict_key = tuples[0]
            else:
                dict_key = (tuples[0:key_number]) # Creates a tuple which will become key of outer dictionary
        else:
            print 'Please provide some keys.'

        final_dictionary[dict_key] = dict_value
    return final_dictionary
