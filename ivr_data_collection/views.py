from django.shortcuts import render
import requests
from models import CustomFieldTest
from django.core import urlresolvers
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
import logging
import json


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
3239:["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/hindi_introduction.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_screening_question.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_adoption_question.wav",["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_non_negotiable_question_1.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_non_negotiable_question_2.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_non_negotiable_question_3.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/bhindi_non_negotiable_question_4.wav"],"https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/hindi_thanks.wav"],
3205:["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/hindi_introduction.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_screening_question.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_adoption_question.wav",["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_non_negotiable_question_1.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_non_negotiable_question_2.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_non_negotiable_question_3.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/moong_non_negotiable_question_4.wav"],"https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi+wavs/hindi_thanks.wav"],
3744:["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhojpuri_introduction.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_screening_question.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_adoption_question.wav",["https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_non_negotiable_1.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_non_negotiable_2.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_non_negotiable_3.wav","https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhindi_non_negotiable_4.wav"],"https://s3.amazonaws.com/dg_ivrs/bihar_pilot/bhojpuri_audios/bhijpuri+wavs/bhojpuri_thanks.wav"],
}
# Create your views here.
def call_exotel(request):
    r = requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'.format(sid=sid),
        auth=(sid, token),
        data={
            'From': 9910338592,
            'CallerId': callerid,
            'TimeLimit': timelimit,
            'Url': url,
            'TimeOut': timeout,
            'CallType': calltype,
            'CustomField': 1
        })
    json_data = json.loads(r.text)
    log_string = "".join(["Call begins : Call id : ", json_data['Call']['Sid'],", Person id : ",person_id, " , videoId : ", videoId])
    logger.debug(log_string)
    return HttpResponse("job done")


def greeting_view(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    log_string = "".join(["Screening Question : Call id : ", callSid, " , videoId : ", videoId])
    logger.debug(log_string)
    response = HttpResponse(videoDetails[int(videoId)][0],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
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
    log_string = "".join(["Screening Question : Call id : ", callSid, " , videoId : ", videoId])
    logger.debug(log_string)
    response = HttpResponse(videoDetails[int(videoId)][1],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response


def screening_answer(request, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    log_string = "".join(["Screening Question : Call id : ", callSid, " , videoId : ", videoId, " option : ", option])
    logger.debug(log_string)
    response = HttpResponse(status=200,content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response

def adoption_question(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    log_string = "".join(["Adoption Question : Call id : ", callSid, " , videoId : ", videoId])
    logger.debug(log_string)
    response = HttpResponse(videoDetails[int(videoId)][2],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response

def adoption_answer(request, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Adoption answer : Call id : " + callSid + " , videoId : " + videoId + " option : " + option)
    response = HttpResponse(status=200,content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response

def nonnegotiable_question(request, num):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Non Negotiable Question :"+ num + " Call id : " + callSid + " , videoId : " + videoId)
    response = HttpResponse(videoDetails[int(videoId)][3][int(num)-1],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response

def nonnegotiable_answer(request, num, option):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Non Negotiable Answer :"+ num + " Call id : " + callSid + " , videoId : " + videoId+ " option : " + option)
    if int(num) >= 4:
        return HttpResponse(status=406)
    response = HttpResponse("",content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response

def thanks(request):
    callSid = request.GET["CallSid"]
    videoId = request.GET["CustomField"]
    frm = request.GET["From"]
    to = request.GET["To"]
    logger = logging.getLogger('ivr_log')
    logger.debug("Call finished : Call id : %s , videoId : %s",callSid,videoId)
    response = HttpResponse(videoDetails[int(videoId)][4],content_type="text/plain")
    response["CallSid"] = callSid
    response["From"] = frm
    response["To"] = to
    response["DialWhomNumber"] = ""
    response["CustomField"] =  videoId
    return response


