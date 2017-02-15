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
from geographies.models import *
from videos.models import *
from qacoco.models import *


class RelationShipDataCategory(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        filename = settings.PROJECT_PATH +'/category-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        #for csv
        abg_adop = None
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow(['ParentCategory',
                             'Category',
                             'SubCategory',
                             'VideoPractice',
                             ])
            vp_obj_list = VideoPractice.objects.values('id', 'videopractice_name',
                                                       'subcategory__subcategory_name',
                                                       'subcategory__category__category_name',
                                                       'subcategory__category__parent_category__parent_category_name',
                                                       )
            for idx, iterable in enumerate(vp_obj_list):
                try:
                    writer.writerow([
                                    iterable.get('subcategory__category__parent_category__parent_category_name'),
                                    iterable.get('subcategory__category__category_name'),
                                    iterable.get('subcategory__subcategory_name'),
                                    iterable.get('videopractice_name')
                                    ])
                except Exception as e:
                    print e

            return response