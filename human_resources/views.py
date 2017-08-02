from django.shortcuts import render_to_response
from django.template import RequestContext
from human_resources.models import ExperienceQualification, Geography, Job, KeyResponsibility, Member

def privacy_policy_view(request):
    context = {
        'header': {
            'jsController':'Team',
            'currentPage':'Team',
            'loggedIn':False
            },}
    return render_to_response('privacy_policy_page.html', context, context_instance=RequestContext(request))

def member_view(request):
    delhi_team = Member.objects.filter(place__name="Headquarters-Delhi")
    elt_team = delhi_team.filter(team="Executive Leadership Team").all().order_by('hierarchy_num')
    tech_team = delhi_team.filter(team="Technology Team").all().order_by('hierarchy_num')
    support_team = delhi_team.filter(team="Support Team").all().order_by('hierarchy_num')
    programs_team = delhi_team.filter(team="Program Team").all().order_by('hierarchy_num')
    other_teams = Member.objects.exclude(place__name="Headquarters-Delhi").order_by('place__name')
    other_teams_list = [{
                            'name':member.name,
                            'designation':member.designation, 
                            'image': {
                                'url': member.image.url,
                            }, 
                            'email':member.email, 
                            'place':member.place.name,
                            'hierarchy_num':member.hierarchy_num,
                        } for member in other_teams]
    other_teams_list = sorted(other_teams_list, key=lambda k: (k['place'], k['hierarchy_num']))
    context = {
        'header': {
            'jsController':'Team',
            'currentPage':'Team',
            'loggedIn':False
            },
        'elt': elt_team,
        'tech': tech_team,
        'support': support_team,
        'programs': programs_team,
        'other_teams': other_teams_list,
    }
    return render_to_response('team_page.html', context, context_instance=RequestContext(request))
  
def job_view(request):
    job_list = Job.objects.all()
    return render_to_response('career.html',{'job_list':job_list, 'header': {'currentPage':'Careers'}}, context_instance=RequestContext(request))
