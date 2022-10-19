# Create your views here.
from dg.settings import PROJECT_PATH
from django.http import HttpResponse


def service_worker(request):
    sw_path = PROJECT_PATH + "/media/" + "serviceworker.js"
    response = HttpResponse(open(sw_path).read(),
                            content_type='application/javascript')
    return response
