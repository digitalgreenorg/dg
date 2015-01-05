import hashlib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from fbconnect.models import FBUser, FBFollowers


@csrf_exempt
def save_fb_user(request):
    if request.method == 'POST':
        fuid = request.POST.get('fuid', None)
        name = request.POST.get('name', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        if not FBUser.objects.filter(fuid=fuid).exists():
            #user already exists..Don't save
            user = FBUser(fuid=fuid, name=name, first_name=first_name, last_name=last_name)
            user.save()
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('ERROR')


@csrf_exempt
def save_follower(request):
    if request.method == 'POST':
        fbuser = request.POST.get('fuid', None)
        person_id = request.POST.get('person_id', None)
        hash = request.POST.get('hash', None)
        m = hashlib.sha256()
        m.update(fbuser + person_id + "dg_farmerbook")
        if hash == m.hexdigest():
            if not FBFollowers.objects.filter(fbuser=fbuser, person=person_id).exists():
                #user already exists..Don't save
                follower = FBFollowers(fbuser=fbuser, person=person_id)
                follower.save()
        else:
            return HttpResponse('ERROR')
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('ERROR')


@csrf_exempt
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
