from django.shortcuts import render
import requests
from models import CustomFieldTest

sid = "digitalgreen2"
token = "421c11b1235067ca30ca87590c80c31eadc46af0"
        # agent_no="9718935868",
        #customerNo="9718935868",
customerNo="9910338592"
callerid="01130018178"
url='http://my.exotel.in/exoml/start/27038'
timelimit="500"  # This is optional
timeout="500" # This is also optional
calltype="trans" # Can be "trans" for transactional and "promo" for promotional content


# Create your views here.
def call_exotel(request):
    req_id = request.GET.get("id")
    vals = CustomFieldTest.objects.get(id__exact=req_id)
    r = requests.post('https://digitalgreen2:421c11b1235067ca30ca87590c80c31eadc46af0@twilix.exotel.in/v1/Accounts/{sid}/Calls/connect'
        data={
            'From': int(vals.mobile_number),
            'CallerId': callerid,
            'TimeLimit': timelimit,
            'Url': url,
            'TimeOut': timeout,
            'CallType': calltype,
            'CustomField': vals.CustomField
        })
    return 1

def greeting_view(request):
    callSid = request.GET["CallSid"]
    frm = request.GET["From"]
    to = request.GET["To"]
    response = HttpResponse("https://s3.amazonaws.com/dg_ivrs/greetingtry.mp3",content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  "pqr"
    return response

def custom_field_update(request):
    callSid = request.GET["CallSid"]
    frm = request.GET["From"]
    to = request.GET["To"]
    response = HttpResponse("https://s3.amazonaws.com/dg_ivrs/greetingtry.mp3",content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  "pqr"
    return response

