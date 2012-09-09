# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import CountryForm,StateForm,DistrictForm,BlockForm,VillageForm

def country_list(request):
    context = RequestContext(request)
    form = CountryForm()
    context.update({'form': form})
    return render_to_response('coco_proto/country.html', context)

def country_list_offline(request):
    context = RequestContext(request)
    form = CountryForm()
    context.update({'form': form})
    return render_to_response('coco_proto/country_offline.html', context)

def state_list(request):
    context = RequestContext(request)
    form = StateForm()
    context.update({'form': form})
    return render_to_response('coco_proto/state.html', context)

def district_list(request):
    context = RequestContext(request)
    form = DistrictForm()
    context.update({'form': form})
    print "here"
    return render_to_response('coco_proto/district.html', context)

def block_list(request):
    context = RequestContext(request)
    form = BlockForm()
    context.update({'form': form})
    return render_to_response('coco_proto/block.html', context)

def village_list(request):
    context = RequestContext(request)
    form = VillageForm()
    context.update({'form': form})
    return render_to_response('coco_proto/village.html', context)