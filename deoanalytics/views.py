# Create your views here.
from django.http import HttpResponse

from dashboard.models import Screening

def index(request):
    noofscreenings = Screening.objects.all()[0]
    '''output = ', '.join([p.question_text for p in latest_question_list])'''
    
    return HttpResponse(noofscreenings)    
    '''return HttpResponse("Hello, world. You're at the DEO index.")'''
