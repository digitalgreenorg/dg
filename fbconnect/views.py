from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from models import *
# Create your views here.
def save_fb_user(request):
    fuid = request.POST['fuid']
    name = request.POST['name']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    if not FBUser.objects.filter(fuid = fuid).exists():
        #user already exists..Don't save
        user = FBUser(fuid=fuid, name=name, first_name = first_name, last_name = last_name)
        user.save()
    return HttpResponse('SUCCESS')