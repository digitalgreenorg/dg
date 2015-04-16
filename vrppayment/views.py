__author__ = 'HP'
import json, datetime

from django.http import HttpResponse

from activities.models import PersonAdoptPractice, Screening, VRPpayment
from coco.models import CocoUser
from people.models import Person
from programs.models import Partner
from geographies.models import District, Block
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    partner = Partner.objects.order_by('partner_name').values('partner_name', 'id')
    context= {
              'header': {
                         'jsController':'VrpPayment',
                         },
              'partner': partner,
              }
    return render_to_response('vrppayment.html' , context, context_instance = RequestContext(request))


def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = District.objects.select_related().filter(block__village__person__partner_id=selectedpartner).values('district_name', 'id').distinct()
    resp = json.dumps({"district": list(districts)})
    return HttpResponse(resp)

def blocksetter(request):
    selecteddistrict = request.GET.get('district', None)
    blocks = Block.objects.filter(district_id=selecteddistrict).values('block_name', 'id')
    resp = json.dumps({"block":list(blocks)})
    return HttpResponse(resp)

def make_vrp_detail_list(custom_object, list_of_vrps):
    animators_disseminations_payments = []
    for var in list_of_vrps:
        count = 0
        vrp_vill_worked = []
        village_work_list = ""
        each_vrp_dict = {}
        animator_name = var[0]
        animator_id = var[1]
        number_of_screening_pervrp = len(custom_object.each_vrp_diss_list(animator_id))
        each_vrp_dict['name'] = animator_name
        each_vrp_dict['diss_count'] = number_of_screening_pervrp
        each_vrp_dict['dissem_detail'] = make_dissemination_list(custom_object, animator_id)
        for element in each_vrp_dict['dissem_detail']:
            if (element['d_village'] not in vrp_vill_worked):
                vrp_vill_worked.append(element['d_village'])
                village_work_list = element['d_village'] + "; " + village_work_list
        each_vrp_dict['village'] = village_work_list
        animators_disseminations_payments.append(each_vrp_dict)
    return animators_disseminations_payments


def make_dissemination_list(custom_object, vrp_id):
    disseminations = custom_object.each_vrp_diss_list(vrp_id)
    dissemination_details = []
    for dissemination in disseminations:
        each_diss_det_dict = {}
        dissemination_grps = dissemination.farmer_groups_targeted.all()
        farmer_attendance = dissemination.farmers_attendance.all()
        farmer_attendance_count = farmer_attendance.count()
        #print custom_object.get_expected_attendance(dissemination_grps.values_list('id', flat=True))
        total_person_expected = 0
        for grp in dissemination_grps:
            total_person_expected += len(Person.objects.filter(group_id=grp.id))
        diss_video_details = make_videos_shown_list(custom_object, dissemination, farmer_attendance.values_list('id', flat=True), farmer_attendance_count)
        each_diss_det_dict['d_id'] = dissemination.id
        each_diss_det_dict['d_date'] = dissemination.date
        each_diss_det_dict['d_attendance'] = farmer_attendance_count
        each_diss_det_dict['d_village'] = dissemination.village.village_name
        each_diss_det_dict['d_expected_attendance'] = total_person_expected
        each_diss_det_dict['videos_shown_detail'] = diss_video_details
        if total_person_expected > 0:
            attendance_perc = farmer_attendance_count * 100 / total_person_expected
            each_diss_det_dict['result_success'] = True if attendance_perc > 60 else False
        else:
            each_diss_det_dict['result_success'] = False
        dissemination_details.append(each_diss_det_dict)
    return dissemination_details


def make_videos_shown_list(custom_object, dissemination, ppl_attending, ppl_attending_count):
    
    #dissemination_video_shown_id = custom_object.get_video_shown_list(diss_id)
    each_diss_vid_arr_detail = []
    #ppl_attending = custom_object.get_diss_attendees(diss_id)
    for video in dissemination.videoes_screened.all():
        custom_object.get_adoption_data(video.id, ppl_attending)
        each_video_adopt_dict = {}
        video_adopted_ppl = custom_object.get_new_adoption_list(dissemination.date)
        video_already_adopted_ppl = custom_object.get_old_adoption_list(dissemination.date)
        each_video_adopt_dict['v_id'] = video.id
        each_video_adopt_dict['v_n_adoptions'] = video_adopted_ppl.count()
        each_video_adopt_dict['v_n_expected_adoptions'] = ppl_attending_count
        denominator = ppl_attending_count - video_already_adopted_ppl.count()
        if (denominator > 0):
            if (((video_adopted_ppl.count() * 100) / denominator) > 30):
                each_video_adopt_dict['v_adoption_success_result'] = True
            else:
                each_video_adopt_dict['v_adoption_success_result'] = False
        else:
            each_video_adopt_dict['v_adoption_success_result'] = False
        each_diss_vid_arr_detail.append(each_video_adopt_dict)
    return each_diss_vid_arr_detail


def makereport(request):
    per_dissemination_rate = 28                     # Amount to be given to VRP for one successful dissemination
    per_adoption_rate = 12                          # Amount to be given to VRP for one successful adoption
    start_date = request.GET.get('startperiod', None)
    end_date = request.GET.get('endperiod', None)
    selectedpartner = request.GET.get('partner', None)
    selectedblock = request.GET.get('block', None)
    custom_object = VRPpayment(selectedpartner, selectedblock, start_date, end_date)
    list_of_vrps = custom_object.get_req_id_vrp()
    complete_data = make_vrp_detail_list(custom_object, list_of_vrps)
    output_array = []
    i = 0
    for each_vrp in complete_data:
        i += 1
        diss_count = 0
        adoption_count = 0
        for each_diss in each_vrp['dissem_detail']:
            if (each_diss['result_success'] == True):
                diss_count = diss_count + 1
            for each_video in each_diss['videos_shown_detail']:
                if (each_video['v_adoption_success_result'] == True):
                    adoption_count = adoption_count + 1
        final_amount = diss_count * per_dissemination_rate + adoption_count * per_adoption_rate
        screening_amount = diss_count*per_dissemination_rate
        adoption_amount  = adoption_count*per_adoption_rate
        temp_arr = [i, each_vrp['name'], each_vrp['village'],len(each_vrp['dissem_detail']), diss_count, screening_amount, adoption_count, adoption_amount, final_amount]
        output_array.append(temp_arr)
    if not output_array:
        report_data = [[0,'NaN', 'No Data Available', '', '','','', '', '']]
        resp = json.dumps({"vrppayment":report_data})
    else:
        report_data = output_array
        resp = json.dumps({"vrppayment":report_data})
    return HttpResponse(resp)