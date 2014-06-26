import datetime
from dimagi.models import error_list
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.dom import minidom

from models import XMLSubmission
from scripts import save_mobile_data

class SubmissionNotSaved(Exception):
    pass


@csrf_exempt
def save_submission(request):
    submission = XMLSubmission()
    submission.xml_data = request.raw_post_data
    submission.submission_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        submission.save()
    except Exception as ex:
        error = ex
    status, msg = save_in_db(submission)
    submission.error_code = status
    submission.error_message = msg
    update_submission(submission)
    try:
        submission.save()
    except Exception as ex:
        error = ex
    return HttpResponse(status=201)


def save_in_db(submission):
    xml_string = submission.xml_data
    xml_parse = minidom.parseString(xml_string)
    if xml_parse.getElementsByTagName('data'):
        data = xml_parse.getElementsByTagName('data')
        if data[0].attributes["name"].value.lower() == 'screening form' :
            status, msg = save_mobile_data.save_screening_data(xml_parse)
        elif data[0].attributes["name"].value.lower() == 'adoption' :
            status, msg = save_mobile_data.save_adoption_data(xml_parse)
    elif devicereport:
        status = error_list['DEVICE_REPORT']
        msg = 'device_report'
    else:
        status = error_list['UNIDENTIFIED_FORM']
        msg = 'error in form'    
    return status, msg


def update_submission(obj):
    if obj.xml_data== '':
        obj.type = "Error"
        obj.app_version = 0
    else:
        data = minidom.parseString(obj.xml_data)
        if data.getElementsByTagName('data'):
            type = data.getElementsByTagName('data')[0].attributes['name'].value
            if type.lower() == 'screening form' or type.lower() == 'screening':
                type= "Screening"
            elif type.lower() == 'adoption form' or type.lower() == 'adoption':
                type= "Adoption"
            
            obj.type = type
            
            version = data.getElementsByTagName('n1:appVersion')[0].childNodes[0].nodeValue
            version = int(version.split('App #')[1].split(' b')[0])
            obj.app_version = version
            
            obj.username = str(data.getElementsByTagName('n0:username')[0].childNodes[0].nodeValue)
            
            start = data.getElementsByTagName('n0:timeStart')[0].childNodes[0].nodeValue.split('T')
            start_date = str(start[0])
            start_time = str(start[1].split('.')[0])
            obj.start_time = start_date+" "+start_time
            
            end = data.getElementsByTagName('n0:timeEnd')[0].childNodes[0].nodeValue.split('T')
            end_date = str(end[0])
            end_time = str(end[1].split('.')[0])
            obj.end_time = end_date+" "+end_time

        elif data.getElementsByTagName('device_report'):
            obj.type = "Report"
            obj.app_version = 0
