from django.shortcuts import *
from django.http import Http404, HttpResponse

#Mindless views for plain HTML pages on the main website

def base_career(request):
    
    return render_to_response('base_career.html')

def base_contact(request):
    
    return render_to_response('base_contact.html')

def base_team(request):
    
    return render_to_response('base_team.html')

def base_team_board(request):
    
    return render_to_response('base_team_board.html')

def base_team_adviser(request):
    
    return render_to_response('base_team_adviser.html')

def base_team_acclaw(request):
    
    return render_to_response('base_team_acclaw.html')

def base_team_intern(request):
    
    return render_to_response('base_team_intern.html')

def base_team_alumni(request):
    
    return render_to_response('base_team_alumni.html')

def base_press(request):
    
    return render_to_response('base_press.html')

def base_partner(request):
    
    return render_to_response('base_partner.html')

def base_career_immediate(request):
    
    return render_to_response('base_career_immediate.html')
