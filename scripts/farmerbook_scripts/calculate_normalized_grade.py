import glob, os
from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
import csv
import numpy

from activities.models import *
from coco.models import *
from geographies.models import *
from programs.models import *
from people.models import *
from videos.models import *

reader = csv.reader(open('grd_file_5_6.csv', 'rb'), delimiter=',')
scores = []
vill_id = []
grades = ['D','C','B','A']
for row in reader:
    scores.append(float(row[8]))
    vill_id.append(str(row[0]))
min_scores = min(scores)
if min > 0:
    for val in scores:
        val -= min_scores
max_scores = max(scores)
for i in range(len(scores)):
        scores[i] /= max_scores
        scores[i] *= 100 
bins = numpy.array([0., 30., 50., 70., 100.])
# index is an index array holding the bin id for each point in A
index = numpy.digitize(scores, bins)
print index
final_grade = []
for i in range(len(index)):
    ind = int(index[i])-1
    if ind > 3:     # in case of a perfect 100 score
        ind = 3
    grade = grades[ind]
    final_grade.append({'id': vill_id[i],
                        'grade': grade})
print final_grade
    



    