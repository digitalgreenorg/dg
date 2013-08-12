from django.shortcuts import render_to_response
from django.template import RequestContext
from human_resources.models import ExperienceQualification ,Job, KeyResponsibility, Member

def member_view(request):
    delhi_team = Member.objects.filter(location="Headquarters-Delhi")
    elt_team = delhi_team.filter(team="Executive Leadership Team").all().order_by('hierarchy_num')
    tech_team = delhi_team.filter(team="Technology Team").all().order_by('hierarchy_num')
    support_team = delhi_team.filter(team="Support Team").all().order_by('hierarchy_num')
    programs_team = delhi_team.filter(team="Program Team").all().order_by('hierarchy_num')
    other_teams = Member.objects.exclude(location="Headquarters-Delhi").order_by('location')
    other_teams_list = [{'name':member.name, 'designation':member.designation, 
                            'image': {'url': member.image.url}, 'email':member.email, 'location':member.location} for member in other_teams]
    context = {
        'elt': elt_team,
        'tech': tech_team,
        'support': support_team,
        'programs': programs_team,
        'other_teams': other_teams_list,
    }
    return render_to_response('team_page.html', context, context_instance=RequestContext(request))
    
def job_view(request):
    job_list = Job.objects.all().order_by('title')
    return render_to_response('career.html',{'job_list':job_list}, context_instance=RequestContext(request))
    