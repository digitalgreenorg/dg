from django.shortcuts import render_to_response
from django.template import RequestContext
from human_resources.models import Member

def member_view(request):
    member_list = Member.objects.all()
    return render_to_response('teammember.html', {'member_list': member_list}, context_instance=RequestContext(request))