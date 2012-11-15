from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from models import *
import hashlib
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

def save_follower(request):
    fbuser = request.POST['fuid']
    person_id = request.POST['person_id']
    hash = request.POST['hash']
    m = hashlib.sha256()
    m.update(fbuser+person_id+"dg_farmerbook")
    if hash == m.hexdigest():
        if not FBFollowers.objects.filter(fbuser = fbuser, person = person_id).exists():
            #user already exists..Don't save
            follower = FBFollowers(fbuser=fbuser, person=person_id)
            follower.save()
    else:
        return HttpResponse('ERROR')
    return HttpResponse('SUCCESS')