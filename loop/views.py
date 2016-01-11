from django.http import  HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponse
from tastypie.models import ApiKey, create_api_key
from loop_data_log import get_latest_timestamp

# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
                api_key.save()
            return HttpResponse(json.dumps({'key':api_key.key, 'timestamp' : get_latest_timestamp()}))
        else:
            return HttpResponse("0", status=401 )
    else:
        return HttpResponse("0", status = 403)
    return HttpResponse("0", status=400)

def home(request):
	print request
	return HttpResponse(request)
