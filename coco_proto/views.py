# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import CountryForm

def country_list(request):
    context = RequestContext(request)
    form = CountryForm()
    context.update({'form': form})
    return render_to_response('coco_proto/country.html', context)