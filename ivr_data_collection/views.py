from django.shortcuts import render
import requests
from models import CustomFieldTest
from django.core import urlresolvers
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
import logging


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

videoDetails = {
3012:["link To Screening Question","Link to adoption Question",["link to nn 1","link to nn2","link to nn3","link to nn4"]],
3013:["link To Screening Question","Link to adoption Question",["link to nn 1","link to nn2","link to nn3","link to nn4"]],
3014:["link To Screening Question","Link to adoption Question",["link to nn 1","link to nn2","link to nn3","link to nn4"]],
3015:["link To Screening Question","Link to adoption Question",["link to nn 1","link to nn2","link to nn3","link to nn4"]],
}
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
	#Todo
    callSid = request.GET["CallSid"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('social_website')
    logger.info("CustomField Received in Greeting: " + request.GET["CustomField"])
    response = HttpResponse("https://s3.amazonaws.com/dg_ivrs/telugu_greeting.wav",content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  "pqr"
    return response

def custom_field_update(request,num):
    # logger = logging.getLogger('social_website')
    # logger.info("CustomField Received in CFupdate 2")
    # logger.info("CustomField Received in CFupdate: " + request.GET["CustomField"])

    # callSid = request.GET["CallSid"]
    frm = request.GET["From"]
    # to = request.GET["To"]
    # response["CallSid"] = callSid
    # response["From"] = frm
    # response["To"] = to
    # response["DialWhomNumber"] = ""
    # response["CustomField"] =  "pqr"
    # vals.CustomField = request.GET["CustomField"]
    # vals.save()
    return HttpResponse(frm)


def screening_question(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Screening Question : Call id : " + callSid + " , videoId : " + videoId)
    response = HttpResponse(videoDetails[int(videoId)][0],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId


def screening_answer(request, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Screening Answer : Call id : " + callSid + " , videoId : " + videoId + " option : " + option)
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId

def adoption_question(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Adoption Question : Call id : " + callSid + " , videoId : " + videoId)
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId

def adoption_answer(request, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Adoption answer : Call id : " + callSid + " , videoId : " + videoId " option : " + option)
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId

def nonnegotiable_question(request, num):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Non Negotiable Question :"+ num + " Call id : " + callSid + " , videoId : " + videoId " option : " + option)
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId

def nonnegotiable_answer(request, num, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId



