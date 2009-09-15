from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
import datetime
import cjson

def hello(request):
	return HttpResponse("Hello world")

def homepage(request):
	return HttpResponse("This is a home page")

def current_datetime(request):
	now = datetime.datetime.now()
	#t = get_template('current_datetime.html')
	##html = "<html><body>It is now %s. </body></html>" %now
	#html = t.render(Context({'current_date':now}))
	#return HttpResponse(html)
	return render_to_response('current_datetime.html',{'current_date':now})

def hours_ahead(reqest,offset):
	try:
		hour_offset = int(offset)
	except ValueError:
		raise Http404()
	next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
	#assert False
	#html = "<html><body>In %s hour(s), it will be %s.<body></html>" % (offset, dt)
	#return HttpResponse(html)
	return render_to_response('hours_ahead.html',locals())



def feed_animators(request, village_id):
        village = Village.objects.get(pk=int(village_id))
	animators = Animator.objects.filter(assigned_villages=village)
	print 'Hello'
		#str = "test" + "\t" + "Model" + "\n" + "test1" + "\t" + "Model1";	
		#print str
		#temp = cjson.encode(str)
		#return HttpResponse(temp, mimetype="text/plain")
        return render_to_response('feeds/animators.txt', {'animators':animators}, mimetype="text/plain")




def feeds_subcat(request, village_id):
	print 'Hello'
        village = Village.objects.get(pk=int(village_id))
	animators = Animator.objects.filter(assigned_villages=village)
	from django.core import serializers
	json_subcat = serializers.serialize("json", animators)
	return HttpResponse(json_subcat, mimetype="application/javascript")
