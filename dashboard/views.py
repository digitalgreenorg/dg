# Create your views here.

from django.shortcuts import render_to_response

def test_view(request):
	#Book.objects.filter(title__icontains=q)
	return render_to_response('results.html',{'body': "hi"})
