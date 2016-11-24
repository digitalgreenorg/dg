# python imports 
import json
import re

TOTAL_NUMBER_OF_PRINTABLE_COLUMNS = 10
NUMBER_OF_SHEETS = 3
NAME_OF_SHEETS = ['Sheet1, Sheet2', 'Sheet3', 'Sheet4']


def write_heading_in_sheet(ws_obj, heading_str, format_str):
    ws_obj.set_column('A:E', 200)
    ws_obj.merge_range('A1:E1', heading_str, format_str)
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
    ws_obj.set_column(col_index, col_index, 30)
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
                                                    row_index=j.get('cell_index')[0],
                                                    col_index=j.get('cell_index')[1],
                                                    label=j.get('label'), format_str=bold)
                            cell_value = [j.get('cell_index')[0], j.get('cell_index')[1]]
                            if j.get('total'):
                                total_value_in_column.append(j.get('cell_index')[1])
                            if j.get('formula') is not None:
                                column_formula_list.append({'formula': j.get('formula'),
                                                            'col_index': j.get('cell_index')[1]})
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


def read_formula_and_write_to_excel(ws_obj, formula, start, end):
    col_index = column_map.get(str(formula.get('col_index')))
    actual_formula = formula.get('formula')
    final_str = '='
    i = 0
    iter_formula = actual_formula.split()
    while i < len(iter_formula):
        #regex matching
        if re.match('[a-zA-Z]+', iter_formula[i]) is not None:
            print "MTCHED CHARS"
            final_str += iter_formula[i] + str(start)
        else:
            print "NOT    MTCHED CHARS"
            final_str += iter_formula[i]    
        i += 1
    ws_obj.write(col_index+str(start) , final_str)
    return


def write_formula_in_values(ws_obj, sheet_data_list, cell_value, formula_list):
    # write the forumla in cell
    start = cell_value[0] + 2
    end = start + len(sheet_data_list) - 1
    temp_start = start
    for item in formula_list:
        start = temp_start
        while start <= end:
            print "FORMULAAAA   :::", item
            read_formula_and_write_to_excel(ws_obj, item, start, end)
            start += 1
    return

def write_total_in_excel_sheet(ws_obj, start, end, formulacolumn_dict, format_str):
    for item in formulacolumn_dict:
        ws_obj.write(end+2, item, '=SUM('+column_map.get(str(item))+str(start)+':'+column_map.get(str(item))+str(end)+')', format_str)
    return

def prepare_value_data(data):
    """
    Process the post data request and breaking into individual sheet data
    """
    data = json.loads(data)
    aggregator_data = data[0]
    commision_data = data[1]
    transport_data = data[2]
    sheet1_file_name = u''+aggregator_data[-1][0]
    sheet2_file_name = u''+commision_data[-1][0]
    sheet3_file_name = u''+transport_data[-1][0]
    aggregator_data = aggregator_data[:len(aggregator_data)-1]
    commision_data = commision_data[:len(commision_data)-1]
    transport_data = transport_data[:len(transport_data)-1]
    name_of_sheets=[sheet1_file_name, sheet2_file_name, sheet3_file_name]
    combined_data = [aggregator_data, commision_data, transport_data]
    combined_dict =  {'combined_data': combined_data,
                      'name_of_sheets': name_of_sheets}
    return combined_dict

header_dict = {'headers': [{'Sheet1':{'columns': [ {'cell_index': [2,0],
                                                    'format': {'bold':1, 'align':'center'},
                                                    'label': 'S No',
                                                    'formula': None,
                                                    },
                                                    {'cell_index': [2,1],
                                                     'total': '',
                                                      'format': {'bold':1, 'align':'center'},
                                                      'label': 'Date',
                                                      'formula': None,
                                                    },
                                                    {'cell_index': [2,2],
                                                      'total': '',
                                                      'format': {'bold':1, 'align':'center'},
                                                      'label': 'Market Value',
                                                      'formula': None,
                                                    },
                                                    {'cell_index': [2,3],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Quantity [Q] (in Kg)',
                                                     'formula': None,
                                                    },
                                                    {'cell_index': [2,4],
                                                     'total': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Farmers',
                                                     'formula': None,
                                                    },
                                                    {'cell_index': [2,5],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Aggregator Payment [AP] (in Rs) (Rs 0.25*Q)',
                                                     'formula': '0.25 * D',
                                                    },

                                                    {'cell_index': [2,6],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Transport Cost [TC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,7],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Farmers\''' Contribution [FC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,8],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Commision Agent Contribution [CAC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,9],
                                                     'total': True,
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Total Payment(in Rs) (AP + TC - FC - CAC)',
                                                     'formula': 'F + G - H - I'
                                                    }],
                                            'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                            }},

                        {'Sheet2':{'columns': [{'cell_index': [2,0],
                                               'total': '',
                                               'format': {'bold':1, 'align':'center'},
                                               'label': 'Date',
                                               'formula': None,
                                               },
                                                {'cell_index': [2,1],
                                                 'total': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Commision Agent',
                                                  'formula': None,
                                                },
                                                {'cell_index': [2,2],
                                                  'total': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Market',
                                                  'formula': None,
                                                },
                                                {'cell_index': [2,3],
                                                 'total': True,
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Quantity [Q] (in Kg)',
                                                 'formula': None,
                                                },
                                                {'cell_index': [2,4],
                                                 'total': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Comission Agent Discount[cad] (in Rs/Kg)',
                                                 'formula': None,
                                                },
                                                {'cell_index': [2,5],
                                                 'total': True,
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Commision Agent Contribution[CAC] (in Rs) (Q*CAD)',
                                                 'formula': 'D * E'
                                                }],
                                   'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                    }
                        },
                        {'Sheet3':{'columns': [{'cell_index': [2,0],
                                               'total': '',
                                               'format': {'bold':1, 'align':'center'},
                                               'label': 'Date',
                                               'formula': None,
                                               },
                                                {'cell_index': [2,1],
                                                 'total': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Market',
                                                  'formula': None,
                                                },
                                                {'cell_index': [2,2],
                                                  'total': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Tranporter',
                                                  'formula': None,
                                                },
                                                {'cell_index': [2,3],
                                                 'total': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Vechile Type',
                                                 'formula': None,
                                                },
                                                {'cell_index': [2,4],
                                                 'total': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Vechile Number',
                                                 'formula': None,
                                                },
                                                {'cell_index': [2,5],
                                                 'total': True,
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Tranport Cost in Rs',
                                                 'formula': None,
                                                }],
                                   'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                    }
                        }],

}

operation_dict = {'+': '+',
                  '-': '-',
                  '*': '*',
                  '/': '/'}


column_map = {
                '0':'A', 
                '1':'B',
                '2':'C',  
                '3':'D', 
                '4':'E', 
                '5':'F', 
                '6':'G', 
                '7':'H', 
                '8':'I',
                '9':'J', 
                '10':'K', 
                '11':'L', 
                '12':'M', 
                '13':'N', 
                '14':'O', 
                '15':'P', 
                '16':'Q', 
                '17':'R', 
                '18':'S', 
                '19':'T', 
                '20':'U',                        
                '21':'V', 
                '22':'W', 
                '23':'X', 
                '24':'Y', 
                '25':'Z' 
              }
