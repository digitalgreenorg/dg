from django.shortcuts import *
from django.http import HttpResponseRedirect


#Mindless views for plain HTML pages on the main website

def home(request):
    return render_to_response('base_home.html')

def aboutus(request):
    return render_to_response('base_aboutusoverview.html')

def career(request):
    return render_to_response('base_career.html')

def career_immediate(request):
    return render_to_response('base_career_immediate.html')

def contact(request):
    return render_to_response('base_contact.html')

def team(request):
    return render_to_response('base_team.html')

def team_board(request):
    return render_to_response('base_team_board.html')

def team_adviser(request):
    return render_to_response('base_team_adviser.html')

def team_acclaw(request):
    return render_to_response('base_team_acclaw.html')

def team_intern(request):
    return render_to_response('base_team_intern.html')

def team_alumni(request):
    return render_to_response('base_team_alumni.html')

def press(request):
    return render_to_response('base_press.html')

def partner(request):
    return render_to_response('base_partner.html')

def partnerselection(request):
    return render_to_response('base_partnerselection.html')

def tech(request):
    return render_to_response('technology.html')

def updates(request):
    return HttpResponseRedirect('http://sites.digitalgreen.org/inside-digital-green/updates')

def nexus(request):
    return HttpResponseRedirect('http://sites.digitalgreen.org/inside-digital-green/nexus')