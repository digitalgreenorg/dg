__author__ = 'Lokesh'

import os.path
import csv
import dg.settings

class initialize_lookup():

    def read_lookup_csv(self):
        file_data = csv.reader(open(os.path.join(dg.settings.MEDIA_ROOT + r'/raw_data_analytics/data_analytics.csv')))
        headers = next(file_data)
        headers.remove('')
        matrix = {}
        for row in file_data:
            sub_matrix = {}
            for i in range(0, len(headers)):
                sub_matrix[headers[i]] = []
                temp = row[i + 1].split('$')
                for t in temp:
                    if '&' in t:
                        andtemp = t.split('&')
                        for vl in andtemp:
                            sub_matrix[headers[i]].append(tuple(vl.split('#')))
                    else:
                        sub_matrix[headers[i]].append(tuple(t.split('#')))
            matrix[row[0]] = sub_matrix
        return matrix

