import json
import xlsxwriter
from django.http import JsonResponse
from io import BytesIO

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db.models import Count, Min, Sum, Avg, Max, F

from tastypie.models import ApiKey, create_api_key
from models import LoopUser, CombinedTransaction, Village, Crop, Mandi, Farmer, DayTransportation, Gaddidar, Transporter, Language, CropLanguage, GaddidarCommission, GaddidarShareOutliers

from loop_data_log import get_latest_timestamp
from loop.payment_template import *
# Create your views here.
HELPLINE_NUMBER = "09891256494"


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        loop_user = LoopUser.objects.filter(user=user)
        if user is not None and user.is_active and loop_user.count() > 0:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_object = get_latest_timestamp()
            return HttpResponse(json.dumps(
                {'key': api_key.key, 'timestamp': str(log_object.timestamp), 'full_name': loop_user[0].name,
                 'mode': loop_user[0].mode, 'helpline': HELPLINE_NUMBER, 'phone_number': loop_user[0].phone_number,
                 'district': loop_user[0].village.block.district.id}))
        else:
            return HttpResponse("0", status=401)
    else:
        return HttpResponse("0", status=403)
    return HttpResponse("0", status=400)


def home(request):
    return render_to_response(request, 'loop_base.html')


def dashboard(request):
    return render(request, 'app_dashboards/loop_dashboard.html')


@csrf_exempt
def write_data_in_workbook(request):
    if request.method == 'POST':
        # this will prepare the data
        formatted_post_data = prepare_value_data(request.body)
        # this will indicate number of sheets
        name_of_sheets = formatted_post_data.get('name_of_sheets')
        combined_data = formatted_post_data.get('combined_data')
        # except wrting begins
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        # selecting a general font
        bold = set_format_for_heading(workbook=workbook,
                                      format_str={'bold':1, 'font_size': 12, 'align': 'center', 'text_wrap': True})
        # for developing exceptions
        try:
            for idx, item in enumerate(name_of_sheets):
                ws = workbook.add_worksheet('Sheet'+ str(idx+1))
                # setting the col width
                align_col_row_width_for_heading(ws_obj=ws, row_number=0, merge_col_width=140, merge_row_width=30)
                # finally merge for heading.At this point headng should be ok
                merge_column_in_excel(ws_obj=ws, first_cell="A1",
                                      second_cell="E2",
                                      heading=name_of_sheets[idx],
                                      format_str=bold)
                # getting the cell value so that we will write values of columns
                cell_value_from_headers = get_headers_from_template_dict(ws, idx, header_dict, bold)
                # finally writing in process
                write_values_to_sheet(ws, combined_data[idx], cell_value_from_headers)
        except Exception as e:
            print e
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response


@csrf_exempt
def download_payment_sheet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        aggregator_data = data[0]
        commision_data = data[1]
        transport_data = data[2]


        sheet1_file_name = u''+aggregator_data[-1][0]
        sheet2_file_name = u''+commision_data[-1][0]
        sheet3_file_name = u''+transport_data[-1][0]


        aggregator_data = aggregator_data[:len(aggregator_data)-1]
        commision_data = commision_data[:len(commision_data)-1]
        transport_data = transport_data[:len(transport_data)-1]



        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        ws = workbook.add_worksheet('Sheet 1')
        ws1 = workbook.add_worksheet('Sheet 2')
        ws2 = workbook.add_worksheet('Sheet 3')

        bold = workbook.add_format({'bold':1, 'align':'center'})
        align = workbook.add_format({'align':'right'})
        total_cell_format = workbook.add_format({'bold':1, 'font_size': 15, 'num_format':'#,##0.0', 'align':'right'})
        tformat = workbook.add_format({'bold':1, 'align':'center', 'valign':'vcenter', 'font_size': 20})

        #setting column and row widths
        ws.set_column('B:G', 140)
        ws.set_row(0, 30)
        ws.set_row(1, 30)

        ws1.set_column('B:F', 100)
        ws1.set_row(0, 30)
        ws1.set_row(1, 30)

        ws2.set_column('B:F', 100)
        ws2.set_row(0, 30)
        ws2.set_row(1, 30)

        


        ws.merge_range('B1:G2',sheet1_file_name ,tformat)
        ws1.merge_range('B1:F2',sheet2_file_name, tformat)
        ws2.merge_range('B1:F2',sheet3_file_name, tformat)




        ws.set_column('B:B', 20)
        ws.set_column('C:C',20)
        ws.set_column('D:D', 30)
        ws.set_column('F:F', 40)
        ws.set_column('G:G', 40)
        ws.set_column('H:H', 40)
        ws.set_column('I:I', 40)
        ws.set_column('J:J', 40)

        ws1.set_column('A:A',30)
        ws1.set_column('B:B', 20)
        ws1.set_column('C:C',20)
        ws1.set_column('D:D', 30)
        ws1.set_column('E:E', 40)
        ws1.set_column('F:F', 40)

        ws2.set_column('A:A',30)
        ws2.set_column('B:B', 20)
        ws2.set_column('C:C',20)
        ws2.set_column('D:D', 30)
        ws2.set_column('E:E', 40)
        ws2.set_column('F:F', 40)


        

        #set column titles of each worksheet
        ws.write('A3','S No', bold)
        ws.write('B3','Date', bold)
        ws.write('C3','Market', bold)
        ws.write('D3','Quantity [Q] (in Kg)', bold)
        ws.write('E3','Farmers', bold)
        ws.write('F3','Aggregator Payment [AP] (in Rs) (Rs 0.25*Q)', bold)
        ws.write('G3','Transport Cost [TC] (in Rs)', bold)
        ws.write('H3','Farmers\''' Contribution [FC] (in Rs)', bold)
        ws.write('I3','Commision Agent Contribution [CAC] (in Rs)', bold)
        ws.write('J3','Total Payment(in Rs) (AP + TC - FC - CAC)', bold)


        ws1.write('A3','Date',bold)
        ws1.write('B3','Commision Agent',bold)
        ws1.write('C3','Market',bold)
        ws1.write('D3','Quantity [Q] (in Kg)',bold)
        ws1.write('E3','Commision Agent Discount [CAD] (in Rs/Kg)',bold)
        ws1.write('F3','Commision Agent Contribution[CAC] (in Rs) (Q*CAD)', bold)


        ws2.write('A3','Date',bold)
        ws2.write('B3','Market',bold)
        ws2.write('C3','Transporter',bold)
        ws2.write('D3','Vehicle Type',bold)
        ws2.write('E3','Vehicle Number',bold)
        ws2.write('F3','Transport Cost (in Rs)', bold)

        row = 3

        #Write data in sheet 1
        for i in range(0,len(aggregator_data)):
            col = 0
            for j in range(0,len(aggregator_data[0])):
                ws.write(row, col, aggregator_data[i][j], align)
                col += 1
            row += 1

        ws.set_column('E:E', None, None, {'hidden':True})
            
        start = 4 
        end = start + len(aggregator_data) - 1
        while start <= end:
            ws.write('F'+str(start), '=D'+str(start)+'*0.25')
            ws.write('J'+str(start), '=F'+str(start)+'+G'+str(start)+'-H'+str(start)+'-I'+str(start))
            start += 1  

        
        #write formulas in sheet 1        
        ws.write(row+2, 0, 'Total', total_cell_format)
        ws.write(row+2, 3, '=SUM(D4:D'+str(end)+')', total_cell_format)
        ws.write(row+2, 5, '=SUM(F4:F'+str(end)+')', total_cell_format)
        ws.write(row+2, 6, '=SUM(G4:G'+str(end)+')', total_cell_format)
        ws.write(row+2, 7, '=SUM(H4:H'+str(end)+')', total_cell_format)
        ws.write(row+2, 8, '=SUM(I4:I'+str(end)+')', total_cell_format)
        ws.write(row+2, 9, '=SUM(J4:J'+str(end)+')', total_cell_format)


        #write data in sheet 2
        row = 3
        for i in range(0,len(commision_data)):
            col = 0
            for j in range(0,len(commision_data[0])):
                ws1.write(row, col, commision_data[i][j], align)
                col += 1
            row += 1

        start = 4
        end = start + len(commision_data) - 1
        while start <= end:
            ws1.write('F'+str(start),'=D'+str(start)+'*E'+str(start))
            start += 1

        ws1.write(row+2, 0, 'Total', total_cell_format)
        ws1.write(row+2, 3, '=SUM(D4:D'+str(end)+')', total_cell_format)
        ws1.write(row+2, 5, '=SUM(F4:F'+str(end)+')', total_cell_format)


        #write data in sheet 3
        row = 3
        for i in range(0,len(transport_data)):
            col = 0
            for j in range(0,len(transport_data[0])):
                ws2.write(row, col, transport_data[i][j], align)
                col += 1
            row += 1

        start = 4
        end = start + len(transport_data) - 1
        formula = '='
        while start<= end:
            formula += 'F'+str(start)+'+'
            start += 1 

        formula = formula[:len(formula)-1]    


        #write formulas in sheet 3
        ws2.write(row+2, 0, 'Total', total_cell_format)
        ws2.write(row+2, 5, formula, total_cell_format)    


        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response


def filter_data(request):
    language = request.GET.get('language')
    aggregators = LoopUser.objects.all().values('user__id', 'name', 'name_en')
    villages = Village.objects.all().values('id', 'village_name', 'village_name_en')
    crops = Crop.objects.all().values('id', 'crop_name')
    crops_lang = CropLanguage.objects.values('crop__id', 'crop_name')
    crops_language = [{'id': obj['crop__id'],
                      'crop_name': obj['crop_name']} for obj in crops_lang]
    mandis = Mandi.objects.all().values('id', 'mandi_name', 'mandi_name_en')
    gaddidars = Gaddidar.objects.all().values(
        'id', 'gaddidar_name', 'gaddidar_name_en')
    transporters = Transporter.objects.values('id', 'transporter_name')
    data_dict = {'transporters': list(transporters), 'aggregators': list(aggregators), 'villages': list(villages), 'crops': list(crops),
                 'mandis': list(mandis), 'gaddidars': list(gaddidars), 'croplanguage': list(crops_language)}
    data = json.dumps(data_dict)
    return HttpResponse(data)


def village_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'farmer__village__village_name').distinct().annotate(Count('farmer', distinct=True), Sum('amount'),
                                                             Sum('quantity'), Count(
                                                                 'date', distinct=True),
                                                             total_farmers=Count('farmer'))
    data = json.dumps(list(transactions))
    return HttpResponse(data)


def aggregator_wise_data(request):

    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    transactions = list(
        CombinedTransaction.objects.filter(**filter_args).values('user_created__id').distinct().annotate(
            Count('farmer', distinct=True), Sum('amount'), Sum(
                'quantity'), Count('date', distinct=True),
            total_farmers=Count('farmer')))
    for i in transactions:
        user = LoopUser.objects.get(user_id=i['user_created__id'])
        i['user_name'] = user.name
    data = json.dumps(transactions)
    return HttpResponse(data)


def crop_wise_data(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    village_ids = request.GET.getlist('village_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["farmer__village__id__in"] = village_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    # crop wise data here
    crops = CombinedTransaction.objects.filter(
        **filter_args).values_list('crop__crop_name', flat=True).distinct()

    transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'date').distinct().annotate(Sum('amount'), Sum('quantity'))
    # crop and aggregator wise data
    crops_aggregators = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'user_created__id').distinct().annotate(amount=Sum('amount'), quantity=Sum('quantity'))
    crops_aggregators_transactions = CombinedTransaction.objects.filter(**filter_args).values(
        'crop__crop_name', 'user_created__id', 'date').distinct().annotate(amount=Sum('amount'), quantity=Sum('quantity'))
    for crop_aggregator in crops_aggregators:
        user = LoopUser.objects.get(
            user_id=crop_aggregator['user_created__id'])
        crop_aggregator['user_name'] = user.name
    dates = CombinedTransaction.objects.filter(**filter_args).values_list(
        'date', flat=True).distinct().order_by('date').annotate(Count('farmer', distinct=True))
    dates_farmer_count = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))
    chart_dict = {'dates': list(dates), 'crops': list(crops), 'transactions': list(transactions), 'farmer_count': list(
        dates_farmer_count), 'crops_aggregators': list(crops_aggregators), 'crops_aggregators_transactions': list(crops_aggregators_transactions)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def total_static_data(request):
    total_volume = CombinedTransaction.objects.all(
    ).aggregate(Sum('quantity'), Sum('amount'))
    total_repeat_farmers = len(CombinedTransaction.objects.values(
        'farmer').annotate(farmer_count=Count('farmer')).exclude(farmer_count=1))
    total_farmers_reached = len(
        CombinedTransaction.objects.values('farmer').distinct())
    total_cluster_reached = len(LoopUser.objects.all())
    total_transportation_cost = DayTransportation.objects.values('date', 'user_created__id', 'mandi__id').annotate(
        Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    gaddidar_share = gaddidar_contribution_for_totat_static_data()

    chart_dict = {'total_volume': total_volume, 'total_farmers_reached': total_farmers_reached,
                  'total_transportation_cost': list(total_transportation_cost), 'total_gaddidar_contribution': gaddidar_share, 'total_cluster_reached': total_cluster_reached, 'total_repeat_farmers': total_repeat_farmers}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def gaddidar_contribution_for_totat_static_data():
    gaddidar_share_list = calculate_gaddidar_share(None, None, None, None)
    total_share = 0
    for entry in gaddidar_share_list:
        total_share += entry['amount']
    return total_share


def calculate_gaddidar_share(start_date, end_date, mandi_list, aggregator_list):

    parameters_dictionary = {'mandi__in': mandi_list}
    parameters_dictionary_for_outliers = {
        'mandi__in': mandi_list, 'aggregator__user__in': aggregator_list}
    parameters_dictionary_for_ct = {'date__gte': start_date, 'date__lte': end_date,
                                    'mandi__in': mandi_list, 'user_created__id__in': aggregator_list}

    arguments_for_ct = {}
    arguments_for_gaddidar_commision = {}
    arguments_for_gaddidar_outliers = {}

    for k, v in parameters_dictionary.items():
        if v:
            arguments_for_gaddidar_commision[k] = v

    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    for k, v in parameters_dictionary_for_outliers.items():
        if v:
            arguments_for_gaddidar_outliers[k] = v

    gc_queryset = GaddidarCommission.objects.filter(
        **arguments_for_gaddidar_commision)
    gso_queryset = GaddidarShareOutliers.objects.filter(
        **arguments_for_gaddidar_outliers)
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'mandi', 'gaddidar__discount_criteria').order_by('-date').annotate(Sum('quantity'), Sum('amount'))
    result = []
    for CT in combined_ct_queryset:
        sum = 0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [x.date for x in gso_queryset]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                                                 'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == 0 and len(gc_list_set) > 0:
                    sum += CT['quantity__sum'] * \
                        gc_list_set[0].discount_percent
                elif len(gc_list_set) > 0:
                    sum += CT['amount__sum'] * gc_list_set[0].discount_percent
            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values_list('amount', flat=True)
                if len(gso_gaddidar_date_aggregator):
                    sum += gso_gaddidar_date_aggregator[0]
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__id': CT[
                      'gaddidar'], 'mandi__id': CT['mandi'], 'amount': sum, 'quantity__sum': CT['quantity__sum']})
    return result


def crop_language_data(request):
    crops = CropLanguage.objects.filter(language=request.GET.get('language'))
    data = json.dumps(crops)

    return HttpResponse(data)


def recent_graphs_data(request):
    stats = CombinedTransaction.objects.values('farmer__id', 'date', 'user_created__id').order_by(
        '-date').annotate(Sum('quantity'), Sum('amount'))
    transportation_cost = DayTransportation.objects.values('date', 'mandi__id', 'user_created__id').order_by(
        '-date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))
    dates = CombinedTransaction.objects.values_list(
        'date', flat=True).distinct().order_by('-date')

    gaddidar_contribution = calculate_gaddidar_share(None, None, None, None)

    chart_dict = {'stats': list(stats), 'transportation_cost': list(
        transportation_cost), 'dates': list(dates), "gaddidar_contribution": gaddidar_contribution}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)
    return HttpResponse(data)


def data_for_drilldown_graphs(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    filter_transportation = {}
    filter_args_no_crops = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
        filter_args_no_crops["date__gte"] = start_date
        filter_transportation["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
        filter_args_no_crops["date__lte"] = end_date
        filter_transportation["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["crop__id__in"] = crop_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    filter_args_no_crops["user_created__id__in"] = aggregator_ids
    filter_args_no_crops["mandi__id__in"] = mandi_ids
    filter_args_no_crops["gaddidar__id__in"] = gaddidar_ids

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    total_repeat_farmers = CombinedTransaction.objects.filter(
        **filter_args).values('user_created__id', 'farmer').annotate(farmer_count=Count('farmer'))
    aggregator_mandi = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'), mandi__id__count=Count('date', distinct=True))
    aggregator_gaddidar = CombinedTransaction.objects.filter(**filter_args).values(
        'user_created__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))

    mandi_gaddidar = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'gaddidar__id').annotate(Sum('quantity'), Sum('amount'))
    mandi_crop = CombinedTransaction.objects.filter(
        **filter_args).values('mandi__id', 'crop__id').annotate(Sum('quantity'), Sum('amount'))

    transportation_cost_mandi = DayTransportation.objects.filter(**filter_transportation).values('date',
                                                                                                 'mandi__id', 'user_created__id').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    crop_prices = list(CombinedTransaction.objects.filter(
        **filter_args).values('crop__crop_name', 'crop__id').annotate(Min('price'), Max('price'), Count('farmer', distinct=True)))
    for crop_obj in crop_prices:
        try:
            crop = CropLanguage.objects.get(crop=crop_obj['crop__id'])
            crop_obj['crop__crop_name_en'] = crop.crop_name
        except CropLanguage.DoesNotExist:
            pass

    mandi_crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'mandi__id').annotate(Min('price'), Max('price'))

    gaddidar_contribution = calculate_gaddidar_share(
        start_date, end_date, mandi_ids, aggregator_ids)

    transactions_details_without_crops = CombinedTransaction.objects.filter(**filter_args_no_crops).values(
        'user_created__id', 'mandi__id').annotate(Sum('quantity'), Sum('amount'), mandi__id__count=Count('date', distinct=True))

    chart_dict = {"total_repeat_farmers": list(total_repeat_farmers), "crop_prices": crop_prices, 'aggregator_mandi': list(aggregator_mandi), 'aggregator_gaddidar': list(aggregator_gaddidar), 'mandi_gaddidar': list(
        mandi_gaddidar), 'mandi_crop': list(mandi_crop),  'transportation_cost_mandi': list(transportation_cost_mandi), "mandi_crop_prices": list(mandi_crop_prices), "gaddidar_contribution": gaddidar_contribution, "transactions_details_without_crops": list(transactions_details_without_crops)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def data_for_line_graph(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    aggregator_ids = request.GET.getlist('aggregator_ids[]')
    crop_ids = request.GET.getlist('crop_ids[]')
    mandi_ids = request.GET.getlist('mandi_ids[]')
    gaddidar_ids = request.GET.getlist('gaddidar_ids[]')
    filter_args = {}
    filter_transportation = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
        filter_transportation["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date
        filter_transportation["date__lte"] = end_date
    filter_args["user_created__id__in"] = aggregator_ids
    filter_args["mandi__id__in"] = mandi_ids
    filter_args["gaddidar__id__in"] = gaddidar_ids

    filter_transportation["user_created__id__in"] = aggregator_ids
    filter_transportation["mandi__id__in"] = mandi_ids

    transport_data = DayTransportation.objects.filter(**filter_transportation).values(
        'date').order_by('date').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    aggregator_data = CombinedTransaction.objects.filter(
        **filter_args).values('date').order_by('date').annotate(Sum('quantity'), Sum('amount'))

    dates = CombinedTransaction.objects.filter(**filter_args).values(
        'date').distinct().order_by('date').annotate(Count('farmer', distinct=True))

    crop_prices = CombinedTransaction.objects.filter(
        **filter_args).values('crop__id', 'date').annotate(Min('price'), Max('price'), Sum('quantity'), Sum('amount'))

    chart_dict = {'transport_data': list(transport_data), 'crop_prices': list(
        crop_prices), 'dates': list(dates), 'aggregator_data': list(aggregator_data)}

    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)


def calculate_gaddidar_share_payments(start_date, end_date):

    parameters_dictionary_for_ct = {
        'date__gte': start_date, 'date__lte': end_date}
    arguments_for_ct = {}
    for k, v in parameters_dictionary_for_ct.items():
        if v:
            arguments_for_ct[k] = v

    gc_queryset = GaddidarCommission.objects.all()
    gso_queryset = GaddidarShareOutliers.objects.all()
    combined_ct_queryset = CombinedTransaction.objects.filter(**arguments_for_ct).values(
        'date', 'user_created_id', 'gaddidar', 'gaddidar__gaddidar_name_en', 'mandi', 'mandi__mandi_name_en', 'gaddidar__discount_criteria').order_by('-date').annotate(Sum('quantity'), Sum('amount'))
    result = []
    for CT in combined_ct_queryset:
        sum = 0
        gc_discount = 0
        user = LoopUser.objects.get(user_id=CT['user_created_id'])
        if CT['date'] not in [gso_obj.date for gso_obj in gso_queryset] or user.id not in [gso_obj.aggregator.id for gso_obj in gso_queryset]:
            try:
                gc_list_set = gc_queryset.filter(start_date__lte=CT['date'], gaddidar=CT[
                                                 'gaddidar']).order_by('-start_date')
                if CT['gaddidar__discount_criteria'] == 0 and len(gc_list_set) > 0:
                    sum += CT['quantity__sum'] * \
                        gc_list_set[0].discount_percent
                    gc_discount = sum / CT['quantity__sum']
                elif len(gc_list_set) > 0:
                    sum += CT['amount__sum'] * gc_list_set[0].discount_percent
                    gc_discount = sum / CT['amount__sum']

            except GaddidarCommission.DoesNotExist:
                pass
        else:
            try:
                gso_gaddidar_date_aggregator = gso_queryset.filter(
                    date=CT['date'], aggregator=user.id, gaddidar=CT['gaddidar']).values_list('amount', flat=True)
                if len(gso_gaddidar_date_aggregator):
                    sum += gso_gaddidar_date_aggregator[0]
                    if CT['gaddidar__discount_criteria'] == 0:
                        gc_discount = sum / CT['quantity__sum']
                    else:
                        gc_discount = sum / CT['amount__sum']
            except GaddidarShareOutliers.DoesNotExist:
                pass
        result.append({'date': CT['date'], 'user_created__id': CT['user_created_id'], 'gaddidar__name': CT[
                      'gaddidar__gaddidar_name_en'], 'mandi__name': CT['mandi__mandi_name_en'], 'amount': sum, 'gaddidar_discount': gc_discount})
    return result


def payments(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    filter_args = {}
    if (start_date != ""):
        filter_args["date__gte"] = start_date
    if (end_date != ""):
        filter_args["date__lte"] = end_date

    aggregator_data = CombinedTransaction.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values(
        'date', 'user_created__id', 'mandi__mandi_name', 'gaddidar__gaddidar_name').annotate(Sum('quantity'), Count('farmer', distinct=True))

    outlier_data = CombinedTransaction.objects.filter(
        **filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en')).values('date', 'user_created__id', 'mandi__mandi_name').annotate(Sum('quantity'), Count('farmer', distinct=True)).annotate(gaddidar__commission__sum=Sum(F('gaddidar__commission') * F("quantity")))

    outlier_transport_data = DayTransportation.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en')).values(
        'date', 'mandi__id','mandi__mandi_name', 'user_created__id').annotate(Sum('transportation_cost'), farmer_share__sum=Avg('farmer_share'))

    outlier_daily_data = CombinedTransaction.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), gaddidar__gaddidar_name=F('gaddidar__gaddidar_name_en')).values('date', 'user_created__id', 'mandi__mandi_name', 'farmer__name', 'crop__crop_name', 'gaddidar__commission', 'price', 'gaddidar__gaddidar_name').annotate(Sum('quantity'))

    transportation_data = DayTransportation.objects.filter(**filter_args).annotate(mandi__mandi_name=F('mandi__mandi_name_en'), transportation_vehicle__vehicle__vehicle_name=F('transportation_vehicle__vehicle__vehicle_name_en')).values(
        'date', 'user_created__id', 'transportation_vehicle__vehicle__vehicle_name', "transportation_vehicle__transporter__transporter_name", 'transportation_vehicle__vehicle_number', 'mandi__mandi_name', 'farmer_share').annotate(Sum('transportation_cost'))

    gaddidar_data = calculate_gaddidar_share_payments(start_date, end_date)

    chart_dict = {'outlier_daily_data': list(outlier_daily_data), 'outlier_data': list(outlier_data), 'outlier_transport_data': list(
        outlier_transport_data), 'gaddidar_data': gaddidar_data, 'aggregator_data': list(aggregator_data), 'transportation_data': list(transportation_data)}
    data = json.dumps(chart_dict, cls=DjangoJSONEncoder)

    return HttpResponse(data)
