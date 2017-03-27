
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

class FetchVideoData(object):
    """
    Prepare the data for export
    """

    def run(export):
        from datetime import datetime
        export = True
        filename = settings.PROJECT_PATH +'/all-video-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        #for csv
        abg_adop = None
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow(['State',
            	             'District',
            				 '#VideoID',
            				 'Title',
            				 'Production Date',
                             'Category',
                             'SubCategory',
                             'VideoPractice',
                             ])
            vid_obj = Video.objects.filter(village__block__district__state__country_id=2)
            for item in vid_obj:
	            try:
	            	writer.writerow([item.village.block.district.state.state_name,
	            					 item.village.block.district.district_name,
	            					 item.id,
	            					 item.title,
	            					 item.production_date.strftime('%Y/%m/%d'),
	            					 item.category.category_name if item.category else None,
	            					 item.subcategory.subcategory_name if item.subcategory else None,
	            					 item.videopractice.videopractice_name if item.videopractice else None])
	            except Exception as e:
	            	print e

            return response


