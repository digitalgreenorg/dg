from django.http import  HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponse
from tastypie.models import ApiKey, create_api_key
from loop_data_log import get_latest_timestamp
from models import LoopUser

# Create your views here.
HELPLINE_NUMBER = "09891256494"

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        loop_user = LoopUser.objects.filter(user = user)
        if user is not None and user.is_active and loop_user.count() > 0:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            log_object = get_latest_timestamp()
            return HttpResponse(json.dumps({'key':api_key.key, 'timestamp' : str(log_object.timestamp), 'name':loop_user[0].name, 'mode' : loop_user[0].mode, 'helpline' : HELPLINE_NUMBER, 'phone_number': loop_user[0].phone_number }))
        else:
            return HttpResponse("0", status=401 )
    else:
        return HttpResponse("0", status = 403)
    return HttpResponse("0", status=400)

def home(request):
	print request
	return HttpResponse(request)
