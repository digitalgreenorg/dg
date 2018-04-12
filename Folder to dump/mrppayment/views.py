from geographies.models import Block
from collections import defaultdict
from vrppayment.views import *

class mrppayment(generic.ListView):
    template_name = 'mrppayment/mrppayment.html'
    context_object_name = 'mrppayment'
    queryset = Animator.objects.filter(role=1)

def partnersetter(request):
    partners = Partner.objects.values('partner_name', 'id').order_by('partner_name')
    return HttpResponse(json.dumps(list(partners)), content_type="application/json")

def districtsetter(request):
    selectedpartner = request.GET.get('partner', None)
    districts = Person.objects.select_related().filter(partner_id=selectedpartner).values(
        'village__block__district__district_name', 'village__block__district__id').distinct()
    return HttpResponse(json.dumps(list(districts)), content_type="application/json")


def blocksetter(request):
    selecteddistrict = request.GET.get('district', None)
    blocks = Block.objects.filter(district__id=selecteddistrict).values('block_name', 'id')
    return HttpResponse(json.dumps(list(blocks)), content_type="application/json")


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
    mrp_list = AnimatorAssignedVillage.objects.filter(animator__partner__partner_name=selectedpartner,
                                               animator__role=1).values('animator__id', 'animator__name',
                                                                        'village__village_name', 'village__id').distinct().order_by(
        'animator__id')
    vrp_list = AnimatorAssignedVillage.objects.filter(animator__partner__partner_name=selectedpartner,
                                                 animator__role=0).values('animator__id', 'animator__name',
                                                                          'village__village_name', 'village__id').distinct().order_by(
        'animator__id')

    mrp_detail = defaultdict(list)
    vrp_detail = defaultdict(list)
    mrp_vrp_detail = defaultdict(list)
    vrp_village_list = defaultdict(list)
    mrp_village_list = defaultdict(list)

    for mrp in mrp_list:
        mrp_detail[(mrp['animator__name'],mrp['animator__id'])].append(mrp['village__id'])

    for vrp in vrp_list:
        vrp_detail[(vrp['animator__name'],vrp['animator__id'])].append(vrp['village__id'])

    for mrp in mrp_detail:
        for village in mrp_detail[mrp]:
            mrp_village_list[village].append(mrp)

    for vrp in vrp_detail:
        for village in vrp_detail[vrp]:
            vrp_village_list[village].append(vrp)

    for village in vrp_village_list:
        if village in mrp_village_list:
            for mrp in mrp_village_list[village]:
                mrp_vrp_detail[mrp].extend(vrp_village_list[village])

    for mrp in mrp_vrp_detail:
        mrp_vrp_detail[mrp] = list(set(mrp_vrp_detail[mrp]))

    custom_object = VRPpayment(partner_id, block_id, start_date, end_date)
    list_of_vrps = list(custom_object.get_req_id_vrp())

    vrp_list_for_given_input = []
    for vrp in list_of_vrps:
        vrp_list_for_given_input.append(vrp)

    mrp_output_array = []
    j = 0

    for mrp in mrp_vrp_detail:
        common_vrps = [val for val in mrp_vrp_detail[mrp] if val in vrp_list_for_given_input]
        if len(common_vrps) > 0:
            j += 1
            complete_data = make_vrp_detail_list(custom_object, common_vrps)
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

            for single_vrp_result in output_array:
                tot_diss += single_vrp_result[3]
                succ_diss += single_vrp_result[4]
                succ_vid_adoption += single_vrp_result[6]
            mrp_screening_amount = per_dissemination_rate * succ_diss
            mrp_adoption_amount = per_adoption_rate * succ_vid_adoption
            tot_amount = mrp_screening_amount + mrp_adoption_amount
            mrp_final_result_arr = [j, mrp[0], tot_diss, succ_diss, mrp_screening_amount, succ_vid_adoption, mrp_adoption_amount,
                     tot_amount]
            mrp_output_array.append(mrp_final_result_arr)

    return HttpResponse(json.dumps({"output": mrp_output_array}), content_type="application/json")


def get_block_id(block):
    b_id = Block.objects.filter(block_name=block).values('id')
    return b_id[0]['id']

def get_partner_id(partner):
    p_id = Partner.objects.filter(partner_name=partner).values('id')
    return p_id[0]['id']
