from models import XMLSubmission

def save_submission(request):
    submission = XMLSubmission()
    submission.xml_data = request.body
    submission.save() 
    return HttpResponse(status=201)
