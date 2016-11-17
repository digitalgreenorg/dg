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

def check_value(val):
    if val is not None and isinstance(val, unicode):
        return val.encode('ascii', 'ignore').decode('ascii')
    else:
        return val

def break_word_value_and_identify_category(value):
    """
    list of strings for related practice.
    """
    data_list = []
    calculated_category_list = []
    calculated_subcategory_list = []
    if value is not None:
        pp_obj = PracticeSector.objects.filter(practice__id=value).values('name')
        if len(pp_obj):
            old_category = pp_obj[0].get('name')
            category_list = Category.objects.filter(category_name__icontains=old_category,
                                                    category_name__isnull=False).values('category_name')
            if len(category_list):
                data_list.append(category_list[0].get('category_name'))
    return data_list


def break_word_value_and_identify_subcategory(value):
    """
    list of strings for related practice.
    """
    data_list = []
    sub_category_list = []
    calculated_category_list = []
    calculated_subcategory_list = []
    if value is not None:
        pp_obj = PracticeSubject.objects.filter(practice__id=value).values('name')        
        if len(pp_obj):
            old_subcategory = pp_obj[0].get('name')
            sub_category_list = \
                SubCategory.objects.filter(subcategory_name__icontains=old_subcategory,
                                           subcategory_name__isnull=False).values('subcategory_name').distinct()
            if len(sub_category_list) > 1:
                data_list.append('LEFT')
            elif len(sub_category_list) == 1:
                data_list.append(sub_category_list[0].get('subcategory_name'))
    return data_list


def break_word_value_and_identify_videopractice(value):
    """
    list of strings for related practice.
    """
    data_list = []
    sub_category_list = []
    calculated_category_list = []
    calculated_subcategory_list = []
    old_videopractice = None
    if value is not None:
        pp_obj = PracticeSubSector.objects.filter(practice__id=value).values('name')        
        if len(pp_obj):
            old_videopractice = pp_obj[0].get('name')
            videopractice_list = \
                VideoPractice.objects.filter(videopractice_name__icontains=old_videopractice,
                                         videopractice_name__isnull=False).values('videopractice_name').distinct()
            if len(videopractice_list) > 1:
                data_list.append('LEFT')
            elif len(videopractice_list) == 1:
                data_list.append(videopractice_list[0].get('videopractice_name'))
    return data_list



def calculate_category(rp, existing_value, list_value):
    category_val = None
    if existing_value is not None:
        category_val = existing_value.encode('ascii', 'ignore').decode('ascii')
        return category_val
    if existing_value is None and rp is not None:
        category_val = list_value[0] if len(list_value) else category_val
    # print "Category>>>", category_val, "RP>>>>", rp, "Existing>>>>", existing_value,"LIST>>>>", list_value
    return category_val

def calculate_subcategory(rp, existing_value, list_value):
    subcategory_val = None
    if existing_value is not None:
        subcategory_val = existing_value.encode('ascii', 'ignore').decode('ascii')
        return subcategory_val
    if existing_value is None and rp is not None:
        subcategory_val = list_value[0] if len(list_value) else subcategory_val
    # print "SubCategory>>>", subcategory_val, "RP>>>>", rp, "Existing>>>>", existing_value,"LIST>>>>", list_value
    return subcategory_val

def calculate_videopractice(rp, existing_value, list_value):
    videopractice_val = None
    if existing_value is not None:
        videopractice_val = existing_value.encode('ascii', 'ignore').decode('ascii')
        return videopractice_val
    if existing_value is None and rp is not None:
        videopractice_val = list_value[0] if len(list_value) else videopractice_val
    print "videopractice>>>", videopractice_val, "RP>>>>", rp, "Existing>>>>", existing_value,"LIST>>>>", list_value
    return videopractice_val


class PracticeMapping(object):
    """
    Prepare the data for export
    """

    def run(export):
        srp_list_value = []
        vrp_list_value = []
        rp_list_value = []
        from datetime import datetime
        rp_list_value = []
        category = None
        subcategory = None
        videopractice = None
        export = True
        filename = settings.PROJECT_PATH +'/video-practice-map-data-' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        data_list = []
        if export:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename=%s' % filename
            outfile = open(filename, 'wb')
            writer = csv.writer(outfile)
            writer.writerow(['State',
                             'District',
                             'Video ID',
                             'Video Name',
                             'Category',
                             'Sub Category',
                             'Practice',
                             ])

            vid_obj = Video.objects.filter(time_created__range=['2016-07-18', '2016-10-31']).values('id', 'title',
                                           'village__block__district__district_name',
                                           'village__block__district__state__state_name',
                                           'village__block__district__state_id',
                                           'village__block__district_id',
                                           'category__category_name', 'subcategory__subcategory_name',
                                           'videopractice_id',
                                           'related_practice_id',
                                           'related_practice__practice_name',
                                           'videopractice__videopractice_name',
                                           ).order_by('-time_created')
            for idx, iterable in enumerate(vid_obj):
                rp = iterable.get('related_practice__practice_name')
                rp_id = iterable.get('related_practice_id')
                if rp is not None:
                    # begin manipulation from here
                    rp_list_value = break_word_value_and_identify_category(rp_id)
                    srp_list_value = break_word_value_and_identify_subcategory(rp_id)
                    vrp_list_value = break_word_value_and_identify_videopractice(rp_id)
                    # category = calculate_category(rp, iterable.get('category__category__name'), rp_list_value)
                    # subcategory = calculate_subcategory(rp, iterable.get('subcategory__subcategory_name'), srp_list_value)
                    # videopractice = calculate_videopractice(rp, iterable.get('videopractice__videopractice_name'), vrp_list_value)
                try:
                    writer.writerow([
                                    check_value(iterable.get('village__block__district__state__state_name')),
                                    check_value(iterable.get('village__block__district__district_name')),
                                    iterable.get('id'),
                                    check_value(iterable.get('title')),
                                    # check_value(iterable.get('related_practice__practice_name')),
                                    check_value(iterable.get('category__category_name')),
                                    check_value(iterable.get('subcategory__subcategory_name')),
                                    check_value(iterable.get('videopractice__videopractice_name')),
                                    
                                    
                                    # check_value(iterable.get('videopractice__videopractice_name')),
                                    ])
                except Exception as e:
                    print e

            return response
