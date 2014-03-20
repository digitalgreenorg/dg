from django.shortcuts import *
from django.http import HttpResponseRedirect
from output.views.common import home_with_analytics
from farmerbook import farmer_book_views
from farmerbook.farmer_book_views import get_leaderboard_data
#Mindless views for plain HTML pages on the main website

def farmerfunda(request):
    return redirect('https://docs.google.com/a/digitalgreen.org/forms/d/1vrg0WObCuJLfLjdV44JnpIFX-ggZk4fCh7di0I8md9w/viewform') 

def home(request):
    return home_with_analytics()
    
def wondervillage(request):
   
    return render_to_response('wondervillage.html') 

def wondervillagegame(request):
   
    return render_to_response('wondervillagegame.html') 

def annualreports(request):
   
    return render_to_response('annualreports.html')    

def featuredfarmer(request):
   
    return render_to_response('base_featuredfarmer.html')

def melissaho(request):
   
    return render_to_response('mellisaho.html')

def eric(request):
   
    return render_to_response('eric.html')

def aishwaryaratan(request):
   
    return render_to_response('aishwaryaratan.html')

def srikantvasan(request):
   
    return render_to_response('srikantvasan.html')

def videopage(request):
   
    return render_to_response('videopage.html')

def searchvideo_result(request):
   
    return render_to_response('searchvideo_result.html')

def aboutus(request):
    
    return render_to_response('base_aboutusoverview.html')

def annualreport09(request):
   
    return render_to_response('annualreport09-10.html')

def annualreport10(request):   
    return render_to_response('annualreport10-11.html')

def annualreport10pdf(request):   
    return render_to_response('annualreport10-11_pdf.html')

def annualletter(request):   
    return render_to_response('annualletter.html')

def annualletter10(request):   
    return render_to_response('annualletter10-11.html')

def projectprogress(request):   
    return render_to_response('projectprogress.html')

def projectprogress10(request):   
    return render_to_response('projectprogress10-11.html')

def partners10(request):   
    return render_to_response('partners10-11.html')

def budgetprogress(request):   
    return render_to_response('budgetprogress.html')

def financial10(request):   
    return render_to_response('financial10-11.html')

def scalability(request):   
    return render_to_response('scalability.html')

def lessonlearned(request):   
    return render_to_response('lessonlearned.html')

def challenge10(request):   
    return render_to_response('challenge10.html')

def keyprinciple(request):
    
    return render_to_response('base_overviewkeyprinciple.html')

def corevalue(request):
    
    return render_to_response('base_overviewcorevalue.html')

def sop(request):    
    return render_to_response('workprocedure.html')

def qualityassurance(request):    
    return render_to_response('qualityassurance.html')

def overviewfarmer(request):    
    return render_to_response('base_overviewfarmer.html')

def overviewdatabase(request):    
    return render_to_response('base_overviewdatabase.html')

def overviewproduction(request):    
    return render_to_response('base_overviewproduction.html')

def overviewsequence(request):    
    return render_to_response('base_overviewsequence.html')

def overviewdiffusion(request):    
    return render_to_response('base_overviewdiffusion.html')

def overviewscalability(request):    
    return render_to_response('base_overviewscalability.html')

def overviewdistribution(request):    
    return render_to_response('base_overviewdistribution.html')

def career(request):    
    return render_to_response('base_career.html')

def careers(request):    
    return render_to_response('base_career.html')

def contact(request):    
    return render_to_response('base_contact.html')

def team(request):    
    return render_to_response('base_team.html')


def teamboard(request):    
    return render_to_response('base_team_board.html')


def teamadviser(request):    
    return render_to_response('base_team_adviser.html')

def teamacclaw(request):    
    return render_to_response('base_team_acclaw.html')

def teamintern(request):    
    return render_to_response('base_team_intern.html')

def teamalumni(request):    
    return render_to_response('base_team_alumni.html')

def teammember(request):    
    return render_to_response('base_team_members.html')

def press(request):
    
    return render_to_response('base_press.html')

def partner(request):
    
    return render_to_response('base_partner.html')

def rfa(request):
   
    return render_to_response('partnerselection.html')

def partnerexecutive(request):
    
    return render_to_response('base_partnerexecutive.html')

def partnerresearch(request):
    
    return render_to_response('base_partnerresearch.html')

def partnerinvestor(request):
    
    return render_to_response('base_partnerinvestor.html')

def partnersupporter(request):
    
    return render_to_response('base_partnersupporter.html')

def careerid(request):
    
    return render_to_response('base_career_id.html')

def careersm(request):
    
    return render_to_response('base_career_sm.html')

def careerpm(request):
    
    return render_to_response('base_career_pm.html')

def careernm(request):
    
    return render_to_response('base_career_nm.html')

def careernpc(request):
    
    return render_to_response('base_career_npc.html')

def careerts(request):
    
    return render_to_response('base_career_ts.html')

def careerqam(request):
    
    return render_to_response('base_career_qam.html')

def careerrse(request):
    
    return render_to_response('base_career_se.html')

def careeradm(request):
    
    return render_to_response('base_career_adm.html')

def careerpca(request):
    
    return render_to_response('base_career_pca.html')

def careerpma(request):
    
    return render_to_response('base_career_pma.html')

def donate(request):
    
    return render_to_response('base_donate.html')

def tech(request):
    
    return render_to_response('technology.html')

def photos(request):
    
    return render_to_response('photos.html')

def webvideos(request):
    return render_to_response('web_videos.html')

def keyfacts(request):
    return render_to_response('key_facts.html')

#farmerbook test urls
def farmerpage(request):
    return render_to_response('farmer_page.html')

def villagepage(request):
    return render_to_response('village_page.html')

def grouppage(request):
    return render_to_response('group_page.html')

def retreat11(request):
    
    return render_to_response('base_team_retreat11.html')

def update(request):
    return HttpResponseRedirect('https://sites.google.com/a/digitalgreen.org/inside-digital-green/updates')

def latestupdate(request):
    return HttpResponseRedirect('https://sites.google.com/a/digitalgreen.org/inside-digital-green/updates/june292010transition')

def nexus(request):
    return HttpResponseRedirect('https://sites.google.com/a/digitalgreen.org/inside-digital-green/nexus')

def spring_analytics(request):
    from activities.models import Screening, PersonAdoptPractice, PersonMeetingAttendance
    from geographies.models import Village
    from programs.models import Partner
    from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
    from videos.models import Video
    from django.db.models import Count, Sum, Max, Min
    import datetime
    
    videos = [10000000021208,10000000021093,10000000021146,10000000021176,10000000021096,10000000021196,10000000021195,10000000021156,10000000021157,10000000021217]
    if request.GET.get('from_date', None) and request.GET.get('to_date', None):
        from_date = request.GET.get('from_date', None)
        to_date = request.GET.get('to_date', None)
    else:
        screenings = Screening.objects.filter(videoes_screened__id__in = videos).values_list('id', flat = True).distinct()
        min_max_date = Screening.objects.filter(id__in = screenings).aggregate(Max('date'), Min('date'))
        from_date = min_max_date['date__min']
        to_date = min_max_date['date__max']        
        
    
    search_box_params = {}
    search_box_params['from_date'] = str(from_date)
    search_box_params['to_date'] = str(to_date)
    search_box_params['is_date_selected'] = 1
    
    screenings = Screening.objects.filter(village__block__district__district_name = 'Keonjhar', videoes_screened__id__in = videos, date__lte = to_date, date__gte = from_date).values_list('id', flat = True).distinct()
    scr = list(screenings)
    viewers = PersonMeetingAttendance.objects.filter(screening__id__in = scr).values_list('person__id', flat=True).distinct()   
    persons = list(viewers)
    groups = PersonGroup.objects.filter(person__in = persons).values_list('id', flat = True)
    adoptions = PersonAdoptPractice.objects.filter(person__village__block__district__district_name = 'Keonjhar', video__id__in = videos, date_of_adoption__lte = to_date, date_of_adoption__gte = from_date).values_list('id', flat = True)
    unique_adoptions = PersonAdoptPractice.objects.filter(person__village__block__district__district_name = 'Keonjhar', video__id__in = videos, date_of_adoption__lte = to_date, date_of_adoption__gte = from_date).values_list('person__id', flat = True).distinct()
    villages  = Village.objects.filter(screening__in = screenings, block__district__district_name = 'Keonjhar').values_list('id', flat = True).distinct()
    from_date = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
    to_date = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')
    days_diff = (to_date - from_date).days
    avg_screenings = float(len(screenings))/ days_diff if days_diff else 0
    total_numbers = {}
    total_numbers.update(adoptions = len(adoptions))
    total_numbers.update(unique_adoptions = len(unique_adoptions))
    total_numbers.update(screenings = len(scr))
    total_numbers.update(videos = len(videos))
    total_numbers.update(viewers = len(persons))
    total_numbers.update(groups = len(groups))
    total_numbers.update(villages = len(villages))
    total_numbers.update(avg_screenings = avg_screenings)
    total_numbers.update(avg_adoption_screening = float(len(adoptions))/ len(screenings) if len(screenings) else 0)
    total_numbers.update(avg_adoption_video = float(len(adoptions))/ len(videos) if len(videos) else 0)
        
    return render_to_response('spring_analytics.html', dict(search_box_params = search_box_params, total_numbers = total_numbers))
