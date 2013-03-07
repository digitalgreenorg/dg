from dashboard.models import *
from django.http import HttpResponse

def update_website(request):
    
   # timestamp = request.GET['timestamp']
    rows = ServerLog.objects.all()
    for row in rows:
        print row
    return HttpResponse("0")