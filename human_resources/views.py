from django.shortcuts import render_to_response
from django.template import RequestContext
from human_resources.models import Member

def member_view(request):
    delhi_team = Member.objects.filter(location="Headquarters-Delhi")
    elt_team = delhi_team.filter(team="Executive Leadership Team").all()
    tech_team = delhi_team.filter(team="Technology Team").all()
    support_team = delhi_team.filter(team="Support Team").all()
    programs_team = delhi_team.filter(team="Program Team").all()
    other_teams = Member.objects.exclude(location="Headquarters-Delhi").order_by('location').values()
    context = {
        'elt': elt_team,
        'tech': tech_team,
        'support': support_team,
        'programs': programs_team,
        'other_teams': other_teams,
    }
    return render_to_response('team_page.html', context, context_instance=RequestContext(request))