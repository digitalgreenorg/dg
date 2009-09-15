# Create your views here.

from django.shortcuts import render_to_response

def feeds_subcat(request, cat_id):
	from django.core import serializers
	json_subcat = serializers.serialize("json", Animator.objects.filter(assigned_villages = cat_id))
	return HttpResponse(json_subcat, mimetype="application/javascript")

def feed_animators(request, village_id):     
	village = Village.objects.get(pk=village_id)
	#models = AutoModel.objects.filter(make=make)     
	animators = Animator.objects.filter(assigned_villages=village)
	return render_to_response('feeds/animators.txt', {'animators':animators}, mimetype="text/plain")
