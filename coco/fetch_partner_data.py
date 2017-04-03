# python imports
import csv
# django imports
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.models import *
from django.db.models import Q
#app imports 
from programs.models import *


class PartnerData(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        filename = settings.PROJECT_PATH +'/partner-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow(['PartnerName',
                             'Data of Association'
                             ])
            partner_obj_list = Partner.objects.values()
            for idx, iterable in enumerate(partner_obj_list):
                try:
                    writer.writerow([
                                    iterable.get('partner_name'),
                                    iterable.get('date_of_association'),
                                    ])
                except Exception as e:
                    print e

            return response