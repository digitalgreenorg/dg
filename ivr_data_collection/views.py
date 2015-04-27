from django.shortcuts import render
import requests
from models import CustomFieldTest

sid = "digitalgreen2"
token = "421c11b1235067ca30ca87590c80c31eadc46af0"
        # agent_no="9718935868",
        #customerNo="9718935868",
customerNo="9910338592"
callerid="01130018178"
url='http://my.exotel.in/exoml/start/27037'
timelimit="500"  # This is optional
timeout="500" # This is also optional
calltype="trans" # Can be "trans" for transactional and "promo" for promotional content


# Create your views here.
def call_exotel(request):
    req_id = request.GET.get("id")
    vals = CustomFieldTest.objects.get(id__exact=req_id)
    r = requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'.format(sid=sid),
        auth=(sid, token),
        data={
            'From': int(vals.mobile_number),
            'CallerId': callerid,
            'TimeLimit': timelimit,
            'Url': url,
            'TimeOut': timeout,
            'CallType': calltype,
            'CustomField': vals.CustomField
        })
    return HttpResponse("job done")


def greeting_view(request):
    callSid = request.GET["CallSid"]
    frm = request.GET["From"]
    to = request.GET["To"]
    response = HttpResponse("https://s3.amazonaws.com/dg_ivrs/telugu_greeting.wav",content_type="text/plain")
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
    vals = CustomFieldTest.objects.get(id__exact=1)
    vals.CustomField = request.GET["CustomField"]
    vals.save()
    return response

