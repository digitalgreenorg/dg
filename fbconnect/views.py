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

def get_fbappid_server_url(request):
    if request.get_host() == "test.digitalgreen.org":
        facebook_app_id = 416481021745150
        server_url = "http://test.digitalgreen.org"
    elif request.get_host() == "www.digitalgreen.org":
        facebook_app_id = 373660286051965
        server_url = "http://www.digitalgreen.org"
    else:
        #for local testing
        facebook_app_id = 422365627816558
        server_url = "http://127.0.0.1:8000"
    return {'facebook_app_id': facebook_app_id, 'server_url': server_url}
    