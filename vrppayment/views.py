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
    blocks = Block.objects.filter(district__id=selecteddistrict).values('block_name', 'id')
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
    print animators_disseminations_payments
    return animators_disseminations_payments


def make_dissemination_list(custom_object, vrp_id):
    dissemination_id = custom_object.each_vrp_diss_list(vrp_id)
    dissemination_details = []
    for diss_id in dissemination_id:
        each_diss_det_dict = {}
        dissemination_grp_id = custom_object.get_grp_ids(diss_id[0])
        ppl_attending = custom_object.get_diss_attendees(diss_id[0])
        diss_attendance = len(ppl_attending)
        total_person_expected = len(custom_object.get_expected_attendance(dissemination_grp_id))
        diss_video_details = make_videos_shown_list(custom_object, diss_id[0], diss_id[1])
        each_diss_det_dict['d_id'] = diss_id[0]
        each_diss_det_dict['d_date'] = diss_id[1]
        each_diss_det_dict['d_attendance'] = diss_attendance
        each_diss_det_dict['d_village'] = diss_id[2]
        each_diss_det_dict['d_expected_attendance'] = total_person_expected
        each_diss_det_dict['videos_shown_detail'] = diss_video_details
        if total_person_expected > 0:
            attendance_perc = diss_attendance * 100 / total_person_expected
            if (attendance_perc > 60):
                each_diss_det_dict['result_success'] = True
            else:
                each_diss_det_dict['result_success'] = False
        else:
            each_diss_det_dict['result_success'] = False
        dissemination_details.append(each_diss_det_dict)
    print dissemination_details
    return dissemination_details


def make_videos_shown_list(custom_object, diss_id, diss_date):
    dissemination_video_shown_id = custom_object.get_video_shown_list(diss_id)
    each_diss_vid_arr_detail = []
    ppl_attending = custom_object.get_diss_attendees(diss_id)
    for vid_id in dissemination_video_shown_id:
        custom_object.get_adoption_data(vid_id, ppl_attending)
        each_video_adopt_dict = {}
        video_adopted_ppl = custom_object.get_new_adoption_list(diss_date)
        video_already_adopted_ppl = custom_object.get_old_adoption_list(diss_date)
        each_video_adopt_dict['v_id'] = vid_id
        each_video_adopt_dict['v_n_adoptions'] = len(video_adopted_ppl)
        each_video_adopt_dict['v_n_expected_adoptions'] = len(ppl_attending)
        denominator = len(ppl_attending) - len(video_already_adopted_ppl)
        if (denominator > 0):
            if (((len(video_adopted_ppl) * 100) / denominator) > 30):
                each_video_adopt_dict['v_adoption_success_result'] = True
            else:
                each_video_adopt_dict['v_adoption_success_result'] = False
        else:
            each_video_adopt_dict['v_adoption_success_result'] = False
        each_diss_vid_arr_detail.append(each_video_adopt_dict)
    print each_diss_vid_arr_detail
    return each_diss_vid_arr_detail


def makereport(request):
    start_date = request.GET.get('startperiod', None)
    end_date = request.GET.get('endperiod', None)
    selectedpartner = request.GET.get('partner', None)
    selectedblock = request.GET.get('block', None)
    print "hello1"
    custom_object = VRPpayment(selectedpartner, selectedblock, start_date, end_date)
    print "hello2"
    list_of_vrps = custom_object.get_req_id_vrp()
    print "hello3"
    complete_data = make_vrp_detail_list(custom_object, list_of_vrps)
    print "hello4"
    output_array = []
    i = 0
    for each_vrp in complete_data:
        i += 1
        print "hello5"
        diss_count = 0
        adoption_count = 0
        for each_diss in each_vrp['dissem_detail']:
            if (each_diss['result_success'] == True):
                diss_count = diss_count + 1
            for each_video in each_diss['videos_shown_detail']:
                if (each_video['v_adoption_success_result'] == True):
                    adoption_count = adoption_count + 1
        final_amount = diss_count * 28 + adoption_count * 12
        temp_arr = [i, each_vrp['name'], each_vrp['village'],len(each_vrp['dissem_detail']), diss_count, adoption_count, final_amount]
        output_array.append(temp_arr)
    print "hello6"
    if not output_array:
        report_data = [[0,'NaN', 'No Data Available', '', '', '', '']]
        resp = json.dumps({"vrppayment":report_data})
    else:
        report_data = output_array
        resp = json.dumps({"vrppayment":report_data})
    return HttpResponse(resp)