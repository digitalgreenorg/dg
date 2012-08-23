from django.http import HttpResponse
from models import XMLSubmission

def save_submission(request):
    submission = XMLSubmission()
    submission.xml_data = request.raw_post_data
    submission.save() 
    return HttpResponse(status=201)
