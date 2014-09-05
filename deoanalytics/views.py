import json, datetime

from django.http import HttpResponse

from coco.models import CocoUser
from programs.models import Partner
from people.models import Animator, AnimatorAssignedVillage, Person
from activities.models import Screening, PersonMeetingAttendance, PersonAdoptPractice, VRPpayment
from geographies.models import District, Block, Village

def partnersetter(request):
    partners = Partner.objects.values('partner_name','id').order_by('partner_name')
    return HttpResponse(json.dumps(list(partners)), mimetype="application/json")
        
def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = Person.objects.select_related().filter(partner_id=selectedpartner).values('village__block__district__district_name', 'village__block__district__id').distinct()
    return HttpResponse(json.dumps(list(districts)), mimetype="application/json")

def blocksetter(request):
    selecteddistrict = request.GET.get('district', None)
    blocks = Block.objects.filter(district__id=selecteddistrict).values('block_name', 'id')
    return HttpResponse(json.dumps(list(blocks)), mimetype="application/json")

# Code for VRP payment tool starts here #

def get_partner_id(partner):
    p_id = Partner.objects.filter(partner_name=partner).values('id')
    return p_id


def get_district_id(district):
    d_id = District.objects.filter(district_name=district).values('id')
    return d_id


def get_block_id(block):
    b_id = Block.objects.filter(block_name=block).values('id')
    return b_id


def make_vrp_detail_list(objec, list_of_vrps, start_period, end_period):
    animators_disseminations_payments = []
    start_yyyy = start_period[:4]
    start_mm = start_period[-2:]
    start_dd = 01
    end_yyyy = end_period[:4]
    end_mm = end_period[-2:]
    end_dd = 01
    print "Date = " + start_yyyy + "-" + start_mm + "-" + str(start_dd)
    print "Date = " + end_yyyy + "-" + end_mm + "-" + str(end_dd)
    for var in list_of_vrps:
        count = 0
        vrp_vill_worked = []
        village_work_list = ""
        each_vrp_dict = {}
        animator_name = var[0]
        animator_id = var[1]
        number_of_screening_pervrp = len(objec.each_vrp_diss_list(animator_id))
        each_vrp_dict['name'] = animator_name
        each_vrp_dict['diss_count'] = number_of_screening_pervrp
        each_vrp_dict['dissem_detail'] = make_dissemination_list(objec, animator_id)
        for element in each_vrp_dict['dissem_detail']:
            if (element['d_village'] not in vrp_vill_worked):
                vrp_vill_worked.append(element['d_village'])
                village_work_list = element['d_village'] + "; " + village_work_list
        each_vrp_dict['village'] = village_work_list
        animators_disseminations_payments.append(each_vrp_dict)
    for case in animators_disseminations_payments:
        print case
    return animators_disseminations_payments


def make_dissemination_list(objec, vrp_id):
    dissemination_id = objec.each_vrp_diss_list(vrp_id)
    dissemination_details = []
    for diss_id in dissemination_id:
        each_diss_det_dict = {}
        dissemination_grp_id = objec.get_grp_ids(diss_id[0])
        ppl_attending = objec.get_diss_attendees(diss_id[0])
        diss_attendance = len(ppl_attending)
        total_person_expected = len(objec.get_expected_attendance(dissemination_grp_id))
        diss_video_details = make_videos_shown_list(objec, diss_id[0], diss_id[1])
        each_diss_det_dict['d_id'] = diss_id[0]
        each_diss_det_dict['d_date'] = diss_id[1]
        each_diss_det_dict['d_attendance'] = diss_attendance
        each_diss_det_dict['d_village'] = diss_id[2]
        each_diss_det_dict['d_expected_attendance'] = total_person_expected
        each_diss_det_dict['videos_shown_detail'] = diss_video_details
        attendance_perc = diss_attendance * 100 / total_person_expected
        if (attendance_perc > 60):
            each_diss_det_dict['result_success'] = True
        else:
            each_diss_det_dict['result_success'] = False
        dissemination_details.append(each_diss_det_dict)
    return dissemination_details


def make_videos_shown_list(objec, diss_id, diss_date):
    dissemination_video_shown_id = objec.get_video_shown_list(diss_id)
    each_diss_vid_arr_detail = []
    ppl_attending = objec.get_diss_attendees(diss_id)
    for vid_id in dissemination_video_shown_id:
        objec.get_adoption_data(vid_id, ppl_attending)
        each_video_adopt_dict = {}
        video_adopted_ppl = objec.get_new_adoption_list(diss_date)
        video_already_adopted_ppl = objec.get_old_adoption_list(diss_date)
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
    return each_diss_vid_arr_detail


def report(request):
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    selectedpartner = request.GET.get('p_name', None)
    selecteddistrict = request.GET.get('d_name', None)
    selectedblock = request.GET.get('b_name', None)
    partner_id = get_partner_id(selectedpartner)
    block_id = get_block_id(selectedblock)
    objec = VRPpayment(partner_id, block_id, "2014-01", "2014-04")
    list_of_vrps = objec.get_req_id_vrp()
    print list_of_vrps
    complete_data = make_vrp_detail_list(objec, list_of_vrps, "2014-01", "2014-04")
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
        final_amount = diss_count * 28 + adoption_count * 12
        temp_arr = [i, each_vrp['name'], each_vrp['village'], diss_count, adoption_count, final_amount]
        output_array.append(temp_arr)
    print output_array
    return HttpResponse(json.dumps({"output": output_array}), content_type="application/json")


# Code for VRP payment tool ends here #


# Code for DEO analytics start here #

def deosetter(request):
    selectedpartner = request.GET.get('partner', None)
    selecteddistrict = request.GET.get('district', None)
    
    deos = CocoUser.objects.filter(partner_id=selectedpartner)
    deos_working_in_selected_district = []
    for deo in deos:
        if deo:
            dist = deo.villages.filter(block__district__id=selecteddistrict)
            if len(dist) > 0:
                deos_working_in_selected_district.append(deo)
    resp = [dict(deo_name=deo.user.username, deo_id=deo.user.id) for deo in deos_working_in_selected_district]
    return HttpResponse(json.dumps(list(resp)), mimetype="application/json")

def deodatasetter(request):
    selecteddeo = request.GET.get('deo',None)
    sdate = request.GET.get ('sdate',None)
    edate = request.GET.get ('edate',None)
    
    slag = "NA"
    alag = "NA"
    
    start_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(edate, "%Y-%m-%d")
        
    Screening_objects = Screening.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date])
    screenings_entrydate = Screening_objects.values_list('time_created', flat=True)
    list_of_screening_entrydates = []
    for screening in screenings_entrydate:
        list_of_screening_entrydates.append(str(screening.date()))
               
    s_dict = dict((i,list_of_screening_entrydates.count(i)) for i in list_of_screening_entrydates)
    
    s_laglist = []
    
    if len(list_of_screening_entrydates)> 0:
        
        for screening in Screening_objects:
            s_lag = screening.time_created.date() - screening.date
            s_laglist.append(s_lag.days)
            
        s_avglag= sum(s_laglist) / float(len(s_laglist))
        
        slag = int(s_avglag)
    
    Adoption_objects = PersonAdoptPractice.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date])
    adoptions_entrydate = Adoption_objects.values_list('time_created', flat=True)
    list_of_adoption_entrydates = []
    for adoption in adoptions_entrydate:
        list_of_adoption_entrydates.append(str(adoption.date()))
        
    a_dict = dict((i,list_of_adoption_entrydates.count(i)) for i in list_of_adoption_entrydates)
       
    a_laglist = []
    
    if len(list_of_adoption_entrydates)> 0:        
        
        for adoption in Adoption_objects:
            a_lag = adoption.time_created.date() - adoption.date_of_adoption
            a_laglist.append(a_lag.days)

        a_avglag= sum(a_laglist) / float(len(a_laglist))
    
        alag = int(a_avglag)       
   
    persons = Person.objects.filter(user_created__username=selecteddeo, time_created__range=[start_date, end_date]).count()  
    
    return HttpResponse(json.dumps({
        "screenings":s_dict,
        "adoptions": a_dict,
        "persons": persons,
        "slag": slag,
        "alag": alag}),
    content_type="application/json")