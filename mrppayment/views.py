from django.views import generic
from people.models import *
from geographies.models import District, Village, Block
from programs.models import Partner
from django.http import HttpResponse
import json, datetime
from activities.models import VRPpayment
from people.models import Animator, Person, AnimatorAssignedVillage
from collections import defaultdict
from vrppayment.views import *


class mrppayment(generic.ListView):
    template_name = 'mrppayment/mrppayment.html'
    context_object_name = 'mrppayment'
    queryset = Animator.objects.filter(role=1)

def partnersetter(request):
    partners = Partner.objects.values('partner_name', 'id').order_by('partner_name')
    return HttpResponse(json.dumps(list(partners)), mimetype="application/json")

def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = Person.objects.select_related().filter(partner_id=selectedpartner).values(
        'village__block__district__district_name', 'village__block__district__id').distinct()
    return HttpResponse(json.dumps(list(districts)), mimetype="application/json")


def blocksetter(request):
    selecteddistrict = request.GET.get('district', None)
    blocks = Block.objects.filter(district__id=selecteddistrict).values('block_name', 'id')
    return HttpResponse(json.dumps(list(blocks)), mimetype="application/json")


def getreport(request):
    per_dissemination_rate = 4  # Amount to be given to VRP for one successful dissemination
    per_adoption_rate = 1  # Amount to be given to VRP for one successful adoption
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    selectedpartner = request.GET.get('partner_name', None)
    selecteddistrict = request.GET.get('district_name', None)
    selectedblock = request.GET.get('block_name', None)
    partner_id = get_partner_id(selectedpartner)
    block_id = get_block_id(selectedblock)
    v = AnimatorAssignedVillage.objects.filter(animator__partner__partner_name=selectedpartner,
                                               animator__role=1).values('animator__name',
                                                                        'village__village_name').distinct().order_by(
        'animator__name')
    t_v = AnimatorAssignedVillage.objects.filter(animator__partner__partner_name=selectedpartner,
                                                 animator__role=0).values('animator__name',
                                                                          'village__village_name').distinct().order_by(
        'animator__name')
    mrp_detail = defaultdict(list)
    vrp_detail = defaultdict(list)
    mrp_vrp_detail = defaultdict(list)
    vrp_v_list = {}
    mrp_v_list = {}

    for e in v:
        # if e['animator__name'] not in mrp_detail :
        mrp_detail[e['animator__name']].append(e['village__village_name'])

    for e in t_v:
        # if e['animator__name'] not in mrp_detail :
        vrp_detail[e['animator__name']].append(e['village__village_name'])

    for e in mrp_detail:
        for t in mrp_detail[e]:
            # list of 
            mrp_v_list[t] = e

    for e in vrp_detail:
        for t in vrp_detail[e]:
            vrp_v_list[t] = e

    # t = [val for val in mrp_v_list if val in vrp_v_list]

    for e in vrp_v_list:
        if e in mrp_v_list:
            mrp_vrp_detail[mrp_v_list[e]].append(vrp_v_list[e])

    # code ends here mrp to vrp
    print partner_id, block_id

    custom_object = VRPpayment(partner_id, block_id, start_date, end_date)
    list_of_vrps = list(custom_object.get_req_id_vrp())

    t = []
    for e in list_of_vrps:
        t.append(e[0])
    mrp_output_array = []
    j = 0
    for mrp in mrp_vrp_detail:
        common_vrps = [val for val in mrp_vrp_detail[mrp] if val in t]
        if len(common_vrps) > 0:
            j += 1
            final_vrp_list = []
            for e in list_of_vrps:
                t_vrp = []
                if e[0] in common_vrps:
                    # print 'removing ', e[0]
                    t_vrp.append(e[0])
                    t_vrp.append(e[1])
                    final_vrp_list.append(t_vrp)

            print 'final_vrp_list'
            for e in final_vrp_list:
                print e[0]
            print 'length after removing', len(final_vrp_list)
            complete_data = make_vrp_detail_list(custom_object, final_vrp_list)
            print 'complete data ', len(complete_data)
            # manipulation on complete_data(JSON format) to get output_array
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
                screening_amount = diss_count * per_dissemination_rate
                adoption_amount = adoption_count * per_adoption_rate
                temp_arr = [i, each_vrp['name'], each_vrp['village'], len(each_vrp['dissem_detail']), diss_count,
                            screening_amount, adoption_count, adoption_amount, final_amount]
                output_array.append(temp_arr)

            tot_diss = 0
            succ_diss = 0
            succ_vid_adoption = 0
            for e in output_array:
                tot_diss += e[3]
                succ_diss += e[4]
                succ_vid_adoption += e[6]
            mrp_screening_amount = 4 * succ_diss
            mrp_adoption_amount = succ_vid_adoption
            tot_amount = mrp_screening_amount + mrp_adoption_amount
            t_arr = [j, mrp, tot_diss, succ_diss, mrp_screening_amount, succ_vid_adoption, mrp_adoption_amount,
                     tot_amount]
            mrp_output_array.append(t_arr)

    return HttpResponse(json.dumps({"output": mrp_output_array}), content_type="application/json")


def get_block_id(block):
    b_id = Block.objects.filter(block_name=block).values('id')
    return b_id[0]['id']

def get_partner_id(partner):
    p_id = Partner.objects.filter(partner_name=partner).values('id')
    return p_id[0]['id']
