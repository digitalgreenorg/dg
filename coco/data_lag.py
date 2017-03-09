# python imports
import csv
# django imports
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.models import *
from django.db.models import Q
#app imports 
from videos.models import *
from activities.models import *
from people.models import *
from geographies.models import *
from videos.models import *
from qacoco.models import *


start_date = datetime.datetime.strptime("2017-02-14", "%Y-%m-%d").date()

class DataLag(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        # filename = settings.PROJECT_PATH +'/data-lag-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        #for csv
        abg_adop = None
        if export:
            # response = HttpResponse(content_type='text/csv')
            # response['Content-Disposition'] = \
            #     'attachment; filename=%s' % filename
            # outfile = open(filename, 'wb')
            # writer = csv.writer(outfile)
            # writer.writerow(['#ScreeningId',
            #                  'Category',
            #                  'SubCategory',
            #                  'VideoPractice',
            #                  ])
            # scr_obj = Screening.objects.filter(village__block__district__state__country_id=1, date__range=["2016-01-31", "2016-12-31"])
            # total_diff_days_per_scr = []
            # for idx, iterable in enumerate(scr_obj):
            #     print iterable
            #     total_diff_days_per_scr.append((iterable.time_created.date() - iterable.date).days)
            # print total_diff_days_per_scr
            adop_obj = PersonAdoptPractice.objects.filter(person__village__block__district__state__country_id=1, date_of_adoption__range=["2016-01-31", "2016-12-31"])
            total_diff_days_per_adop = []
            for idx, iterable in enumerate(adop_obj):
                print iterable
                total_diff_days_per_adop.append((iterable.time_created.date() - iterable.date_of_adoption).days)
            print total_diff_days_per_adop
            print sum(total_diff_days_per_adop)    


