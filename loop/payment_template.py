# python imports 
import json

TOTAL_NUMBER_OF_PRINTABLE_COLUMNS = 10
NUMBER_OF_SHEETS = 3
NAME_OF_SHEETS = ['Sheet1, Sheet2', 'Sheet3', 'Sheet4']


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
                        except Exception as e:
                            print e
    return cell_value

def write_values_to_sheet(ws_obj, sheet_data_list, cell_value):
    """
    Write Values to sheets
    """
    row = cell_value[0] + 1
    for i in range(0,len(sheet_data_list)):
        col = 0
        for j in range(0,len(sheet_data_list[0])):
            ws_obj.write(row, col, sheet_data_list[i][j])
            col += 1
        row += 1
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

header_dict = {'headers': [{'Sheet1':{'columns': [{'cell_index': [2,0],
                                                   'formula': '',
                                                   'format': {'bold':1, 'align':'center'},
                                                   'label': 'S No'
                                                   },
                                                    {'cell_index': [2,1],
                                                     'formula': '',
                                                      'format': {'bold':1, 'align':'center'},
                                                      'label': 'Date'
                                                    },
                                                    {'cell_index': [2,2],
                                                      'formula': '',
                                                      'format': {'bold':1, 'align':'center'},
                                                      'label': 'Market Value'
                                                    },
                                                    {'cell_index': [2,3],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Quantity [Q] (in Kg)'
                                                    },
                                                    {'cell_index': [2,4],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Farmers'
                                                    },
                                                    {'cell_index': [2,5],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Aggregator Payment [AP] (in Rs) (Rs 0.25*Q)'
                                                    },

                                                    {'cell_index': [2,6],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Transport Cost [TC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,7],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Farmers\''' Contribution [FC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,8],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Commision Agent Contribution [CAC] (in Rs)'
                                                    },
                                                    {'cell_index': [2,9],
                                                     'formula': '',
                                                     'format': {'bold':1, 'align':'center'},
                                                     'label': 'Total Payment(in Rs) (AP + TC - FC - CAC)',
                                                     'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                                    }],
                                            'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                            }},

                        {'Sheet2':{'columns': [{'cell_index': [2,0],
                                               'formula': '',
                                               'format': {'bold':1, 'align':'center'},
                                               'label': 'Date'
                                               },
                                                {'cell_index': [2,1],
                                                 'formula': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Commision Agent'
                                                },
                                                {'cell_index': [2,2],
                                                  'formula': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Market'
                                                },
                                                {'cell_index': [2,3],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Quantity [Q] (in Kg)'
                                                },
                                                {'cell_index': [2,4],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Comission Agent Discount[cad] (in Rs/Kg)'
                                                },
                                                {'cell_index': [2,5],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Commision Agent Contribution[CAC] (in Rs) (Q*CAD)'
                                                }],
                                   'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                    }
                        },
                        {'Sheet3':{'columns': [{'cell_index': [2,0],
                                               'formula': '',
                                               'format': {'bold':1, 'align':'center'},
                                               'label': 'Date'
                                               },
                                                {'cell_index': [2,1],
                                                 'formula': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Market'
                                                },
                                                {'cell_index': [2,2],
                                                  'formula': '',
                                                  'format': {'bold':1, 'align':'center'},
                                                  'label': 'Tranporter'
                                                },
                                                {'cell_index': [2,3],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Vechile Type'
                                                },
                                                {'cell_index': [2,4],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Vechile Number'
                                                },
                                                {'cell_index': [2,5],
                                                 'formula': '',
                                                 'format': {'bold':1, 'align':'center'},
                                                 'label': 'Tranport Cost in Rs'
                                                }],
                                   'data': [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['11', '21', '31', '41', '51', '61', '71', '8', '9', '10']]
                                    }
                        }],


                                            }



# HEADINGS_OF_SHEETS = [{'Sheet1':
#                               {'heading': 'HEADING1',
#                                'merge_row_width_for_heading': 1,
#                                'merge_column_width_for_heading': 1,
#                                'row_index': '',
#                                'col_index': '',
#                                'format': '(bold, 12)',
#                                'columns':[
#                                           {'first_label':'ABC', 'formula': 'SUM()',
#                                            'column_total': True, 'value': 'value_of_cell'}
#                                           {'second':'DEF', 'printable': 'yes', 'formula': 'TOTAL()',
#                                            'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                            'width': '2-column'},
#                                           {'third':'GHI', 'printable': 'no', 'formula': 'COUNT()',
#                                            'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                            'width': '2-column'},
#                                           ],
#                               'data': '',
#                               }
#                     },
#                     {'Sheet2':
#                               {'heading': 'HEADING2',
#                                'merge_row_width_for_heading': 2,
#                                'merge_column_width_for_heading': 10,
#                                'columns':[
#                                           {'first_label':'XYZ', 'printable': 'yes', 'formula': 'SUM()',
#                                            'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                            'width': '2-column'},
#                                           {'second':'VEU', 'printable': 'yes', 'formula': 'TOTAL()',
#                                            'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                            'width': '2-column'},
#                                           {'third':'IOR', 'printable': 'no', 'formula': 'COUNT()',
#                                            'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                            'width': '2-column'},
#                                          ]
#                               }
#                     },
#                     {'Sheet3':
#                               {'heading': 'HEADING3',
#                               'merge_row_width_for_heading': 2,
#                               'merge_column_width_for_heading': 10,
#                               'columns':[
#                                         {'first_label':'ABC', 'printable': 'yes', 'formula': 'SUM()',
#                                          'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                          'width': '2-column'},
#                                         {'second':'DEF', 'printable': 'yes', 'formula': 'TOTAL()',
#                                          'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                          'width': '2-column'},
#                                         {'third':'GHI', 'printable': 'no', 'formula': 'COUNT()',
#                                          'format': {'Helvitca', 'font_size': 12}, 'column_total': True,
#                                          'width': '2-column'},
#                                        ]
#                               }
#                     }]




# COLUMN_OF_SHEETS = {'Sheet1':[
#                             {'columns':[
#                                         {'first_column':'ABC', 'printable': 'yes', 'formula': 'SUM()',
#                                         'font_size': 12, 'font_style': 'Helvitca', 'column_total': True},
#                                         {'first_column':'DEF', 'printable': 'yes', 'formula': 'TOTAL()',
#                                         'font_size': 12, 'font_style': 'Helvitca', 'column_total': False}
#                                         {'first_column':'GHI', 'printable': 'no', 'formula': 'COUNT()',
#                                         'font_size': 12, 'font_style': 'Helvitca', 'column_total': True}
#                                        ],
#                              },

#                            ]}