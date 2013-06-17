# Create your views here.
from django.contrib import auth
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render

def test_view(request):
	#Book.objects.filter(title__icontains=q)
	return render_to_response('results.html',{'body': "hi"})

def coco_v2(request):
    return render(request,'dashboard.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    return HttpResponse("1")
    
def logout(request):
    auth.logout(request)    
    return HttpResponse("1")