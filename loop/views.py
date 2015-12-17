from django.http import  HttpResponse

def home(request):
	print request
	return HttpResponse(request)
