# python imports
import csv
import datetime
# django imports
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.db.models import *
from django.db.models import Q
#app imports 
from videos.models import *
from people.models import *
from geographies.models import *
from videos.models import *
from qacoco.models import *


start_date = datetime.datetime.strptime("2017-02-14", "%Y-%m-%d").date()

class InsertHNNData(object):
    """
    Prepare the data for export
    """

    def create_geography(data_list):
        
        
        state_name = data_list[0]
        district_name = data_list[1]
        block_name = data_list[2]
        village_name = data_list[3]

        country, created = \
            Country.objects.get_or_create(country_id=1,
                                          start_date=start_date)
        state, created = \
            State.objects.get_or_create(name=state_name,
                                        start_date=start_date,
                                        country=country)
        district, created = \
            District.objects.get_or_create(name=district_name,
                                           start_date=start_date,
                                           state=state)
        block, created = \
            Block.objects.get_or_create(name=block_name,
                                        district=district,
                                        start_date=start_date)
        village, created = \
            Village.objects.get_or_create(name=village_name,
                                          block=block,
                                          start_date=start_date) 
        return obj


    def run(export):
        from datetime import datetime
        export = True
        filename = csv.reader(open(settings.PROJECT_PATH +'/data_to_be_inserted.csv', 'rU'), dialect=csv.excel_tab, delimiter=',')
        data_list = []
        #for csv
        abg_adop = None
        if export:
            # response = HttpResponse(content_type='text/csv')
            # response['Content-Disposition'] = \
            #     'attachment; filename=%s' % filename
            # outfile = open(filename, 'wb')
            next(filename)
            for row_idx, row in enumerate(filename):
                try:
                    print row_idx, row[1]
                    data_list = row
                    state_name = data_list[0]
                    district_name = data_list[1]
                    block_name = data_list[2]
                    village_name = data_list[3]
                    group_name = data_list[4]
                    mediator_name = data_list[5]
                    gender = data_list[6]
                    person_name = data_list[7]
                    father_name = data_list[8]
                    person_gender = data_list[9]


                    country, created = \
                        Country.objects.get_or_create(id=1)
                    
                    state, created = \
                        State.objects.get_or_create(state_name=state_name,
                                                    country=country)
                    state.start_date = start_date
                    state.save()

                    district, created = \
                        District.objects.get_or_create(district_name=district_name,
                                                       state=state)
                    district.start_date = start_date
                    district.save()
                    block, created = \
                        Block.objects.get_or_create(block_name=block_name,
                                                    district=district,
                                                    )
                    block.start_date = start_date
                    block.save()
                    village, created = \
                        Village.objects.get_or_create(village_name=village_name,
                                                      block=block,
                                                      )
                    village.start_date = start_date
                    village.save()
                    
                    group_obj, created = \
                        PersonGroup.objects.get_or_create(group_name=group_name,
                                                          village=village,
                                                          partner_id=24)
                    # group_obj.partner_id=24
                    # group_obj.save()

                    if gender == "Female":
                        gender = 'F'
                    else:
                        gender = "M"

                    if person_gender == "Female":
                        person_gender = "F"
                    else:
                        person_gender = "M"
                    # import pdb;pdb.set_trace()
                    mediator_obj, created = \
                        Animator.objects.get_or_create(name=mediator_name,
                                                       gender=gender,
                                                       partner_id=24,
                                                       district=district)
                    ani_obj, created = \
                        AnimatorAssignedVillage.objects.get_or_create(village=village,
                                                                      animator=mediator_obj)
                    # mediator_obj.assigned_villages = ani_obj
                    # mediator_obj.save()
                    person_obj, created = \
                        Person.objects.get_or_create(person_name=person_name,
                                                     father_name=father_name,
                                                     gender=gender,
                                                     village=village,
                                                     group=group_obj,
                                                     partner_id=24)



                except Exception as e:
                    print e