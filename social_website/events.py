from django.http import HttpResponse

def event_registration(request):
    print request.POST
    message = "All Good!"
    return HttpResponse(message)

