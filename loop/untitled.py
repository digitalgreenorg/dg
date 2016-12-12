        for i in header_dict:
            for k in header_dict[i]:
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