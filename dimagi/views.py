from django.http import HttpResponse
from models import XMLSubmission
from xml.dom import minidom
from scripts import save_mobile_data

def save_submission(request):
    submission = XMLSubmission()
    submission.xml_data = request.raw_post_data
    submission.save() 
    status, msg = save_in_db(submission)
    submission.error_code = status
    submission.error_message = msg
    submission.save()
#    try:
#        submission.save()
#    except Exception as ex:
#        error = ex
    return HttpResponse(status=201)


def save_in_db(submission):
    xml_string = submission.xml_data
    xml_parse = minidom.parseString(xml_string)
    data = xml_parse.getElementsByTagName('data')
    if data[0].attributes["name"].value.lower() == 'screening' :
        status, msg = save_mobile_data.save_screening_data(xml_parse)
        
    elif data[0].attributes["name"].value.lower() == 'adoption' :
        status, msg = save_mobile_data.save_adoption_data(xml_parse)
    else :
        status = -1
        msg = 'error in form'
    return status, msg
