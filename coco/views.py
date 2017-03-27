from datetime import datetime
from django.contrib import auth
from django.core import urlresolvers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, render
from coco.models import FullDownloadStats
from models import CocoUser
from forms import DataUploadForm
import xlrd
from os.path import join, dirname, abspath
import dg.settings
import json
import re
from django.db.models import Q

from people.models import Person,Animator,AnimatorAssignedVillage
from people.models import PersonGroup
from geographies.models import Village,District
from programs.models import Partner
from videos.models import Video,Language,Category,Practice,SubCategory
from activities.models import Screening,PersonAdoptPractice

def coco_v2(request):
    return render(request,'dashboard.html')
    
def login(request):
    partner_name = None
    type_of_cocouser = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            coco_user_obj = CocoUser.objects.filter(user_id=request.user.id)
            if len(coco_user_obj):
                partner_name = coco_user_obj[0].partner.partner_name.lower()
                type_of_cocouser = coco_user_obj[0].type_of_cocouser
        else:
            return HttpResponse("0")
    else:
        return HttpResponse("0")
    return JsonResponse({'success': '1', 'partner_name': partner_name, 'type_of_cocouser': type_of_cocouser})
    
def logout(request):
    auth.logout(request)    
    return HttpResponse("1")
   
def record_full_download_time(request):
    if not(request.user and request.POST["start_time"] and request.POST["end_time"]):
        return HttpResponse("0")
    stat = FullDownloadStats(user = request.user, start_time = request.POST["start_time"], end_time = request.POST["end_time"])
    stat.save()
    return HttpResponse("1")
       
def reset_database_check(request):
    if not request.user.is_authenticated():
        return HttpResponse("0")
    cocouser = CocoUser.objects.get(user = request.user)
    if not(cocouser and cocouser.time_modified):
        return HttpResponse("0")
    lastdownloadtime = request.GET["lastdownloadtimestamp"]
    lastdownloadtimestamp = datetime.strptime(lastdownloadtime, '%Y-%m-%dT%H:%M:%S.%f')
    if lastdownloadtimestamp <= cocouser.time_modified:
        return HttpResponse("1")
    return HttpResponse("0")
    
               
def html_decorator(func):
    """
    This decorator wraps the output in html.
    (From http://stackoverflow.com/a/14647943)
    """
 
    def _decorated(*args, **kwargs):
        response = func(*args, **kwargs)
 
        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")
 
        return HttpResponse(wrapped)
 
    return _decorated
 
@html_decorator
def debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("debug/", "")
 
    view = urlresolvers.resolve(api_url)
 
    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept
 
    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)


def upload_data(request):
    if request.method == 'POST':
        form_data = DataUploadForm(request.POST, request.FILES)
        if form_data.is_valid():
            cd = form_data.cleaned_data
            print request.FILES
            document_raw = Document(docfile = request.FILES['csvfile'])
            document_raw.save()
            read_xlsx(document_raw)
            #return HttpResponseRedirect(".")
    else:
        form_data = DataUploadForm()
    context = {'form': form_data}
    template = "coco/data_upload.html"
    return render(request, template, context)
 
def read_xlsx(document):
    document_docfile_name = join(dg.settings.MEDIA_ROOT,document.docfile.name)
    wb = xlrd.open_workbook(document_docfile_name)
    worksheets = ['group']
    usersheet = wb.sheet_by_name('user')
    userdict = {}
    for i in range(1,usersheet.ncols):
        key = usersheet.cell(0,i).value
        value = usersheet.cell(1,i).value
        userdict[key] = value

    
    partnerObject = Partner.objects.get(partner_name=userdict['partner_name'])    
    data=[]
    ###Group Upload###
    sheet = wb.sheet_by_name('group')
    rowcount = sheet.nrows
    colcount = sheet.ncols
    for row in range(1,rowcount):
        sheetdict= {}
        for col in range(0,colcount):
            key = sheet.cell(0,col).value
            value = sheet.cell(row,col).value
            if value =='null':
                value=None
            sheetdict[key] = value
        village = json.loads(str(sheetdict['village']))
        villageObject = Village.objects.get(id=village['id'])
        if sheetdict['online_id']=='':
            groupObject = PersonGroup(group_name=sheetdict['group_name'],village =villageObject,partner=partnerObject)
            groupObject.save()
        else:
            groupObject = PersonGroup.objects.get(id=sheetdict['online_id'])
            groupObject.group_name=sheetdict['group_name']
            groupObject.village=villageObject
            groupObject.save()

    data=[]
    ###Video Upload###
    sheet = wb.sheet_by_name('video')
    rowcount = sheet.nrows
    colcount = sheet.ncols
    for row in range(1,rowcount):
        sheetdict= {}
        for col in range(0,colcount):
            key = sheet.cell(0,col).value
            value = sheet.cell(row,col).value
            if value =='null':
                value=None
            sheetdict[key] = value
        prod = json.loads(str(sheetdict['production_team']))
        productionteamList=[]
        for i in prod:
            productionteamList.append(str(i['id']))
        listprodteam=[]
        listprodteam=list(Animator.objects.filter(Q(id__in=productionteamList)))
        village = json.loads(str(sheetdict['village']))
        villageObject = Village.objects.get(id=village['id'])
        language =json.loads(str(sheetdict['language']))
        languageObject = Language.objects.get(id=language['id'])
        approval_date = sheetdict['approval_date']
        benefit = sheetdict['benefit']
        category = json.loads(str(sheetdict['category']))
        category_id = category['id']
        try:
            categoryObject = Category.objects.get(id=category_id)    
        except:
            categoryObject = None
        practice = json.loads(str(sheetdict['videopractice']))
        practice_id = practice['id']
        try:
            practiceObject = Practice.objects.get(id=practice_id)
        except:
            practiceObject = None
        video_type = sheetdict['video_type']
        title = sheetdict['title']
        subCategory = json.loads(str(sheetdict['subcategory']))
        SubCategory_id = subCategory['id']
        try:
            SubCategoryObject = SubCategory.objects.get(id=SubCategory_id)  
        except:
            SubCategoryObject = None
        reviewer = sheetdict['reviewer']
        reviewed_by = sheetdict['reviewed_by']
        youtubeid = sheetdict['youtubeid']
        production_date = sheetdict['production_date']

        if sheetdict['online_id']=='':
            videoObject = Video(title=title,video_type=video_type,youtubeid=youtubeid,production_date=production_date,language=languageObject,village=villageObject,reviewed_by=reviewed_by,reviewer=reviewer,practice=practiceObject,category=categoryObject,subcategory=SubCategoryObject,benefit=benefit,approval_date=approval_date,partner=partnerObject)
            videoObject.save()
            videoObject.production_team.add(*listprodteam)
        else:
            videoObject = Video.objects.get(id=sheetdict['online_id'])
            videoObject.title = title
            videoObject.production_date = production_date
            videoObject.language = languageObject
            videoObject.village = villageObject
            videoObject.video_type = video_type
            videoObject.youtubeid = youtubeid
            videoObject.reviewed_by = reviewed_by
            videoObject.reviewer = reviewer
            videoObject.practice = practiceObject
            videoObject.category = categoryObject
            videoObject.subcategory = SubCategoryObject
            videoObject.benefit = benefit
            videoObject.approval_date = approval_date
            videoObject.save()
            videoObject.production_team.add(*listprodteam)


    data = []
    sheet = wb.sheet_by_name('mediator')
    rowcount = sheet.nrows
    colcount = sheet.ncols
    for row in range(1,rowcount):
        sheetdict= {}
        for col in range(0,colcount):
            key = sheet.cell(0,col).value
            value = sheet.cell(row,col).value
            if value =='null':
                value=None
            sheetdict[key] = value
        assignedvillage = json.loads(str(sheetdict['assigned_villages']))
        villageList=[]
        for i in assignedvillage:
            villageList.append(str(i['id']))
        listvillage=[]
        listvillage=list(Village.objects.filter(Q(id__in=villageList)))
        phone_number = sheetdict['phone_no']
        name =  sheetdict['name']
        district = json.loads(str(sheetdict['district']))
        districtObject = District.objects.get(id=district['id'])
        gender = sheetdict['gender']
        role = sheetdict['role']
        if sheetdict['online_id']=='':
            animatorObject = Animator(name=name,district=districtObject,role=role,gender=gender,phone_no=phone_number,partner=partnerObject)
            animatorObject.save()
            for obj in listvillage:
                AnimatorAssignedVillage.objects.get_or_create(animator=animatorObject,village=obj)
        else:
            animatorObject = Animator.objects.get(id=sheetdict['online_id'])
            animatorObject.name = name
            animatorObject.gender = gender
            animatorObject.role = role
            animatorObject.district = districtObject
            animatorObject.save()
            for obj in listvillage:
                AnimatorAssignedVillage.objects.get_or_create(animator=animatorObject,village=obj)


    data = []
    sheet = wb.sheet_by_name('screening')
    rowcount = sheet.nrows
    colcount = sheet.ncols
    for row in range(1,rowcount):
        sheetdict= {}
        for col in range(0,colcount):
            key = sheet.cell(0,col).value
            value = sheet.cell(row,col).value
            if value =='null':
                value=None
            sheetdict[key] = value
        
        start_time = sheetdict['start_time']
        date = sheetdict['date']
        village = json.loads(str(sheetdict['village']))
        villageObject = Village.objects.get(id=village['id'])
        animator = json.loads(str(sheetdict['animator']))
        animatorObject = Animator.objects.get(id=animator['id'])
        videoesscreened = json.loads(str(sheetdict['videoes_screened']))
        videoList=[]
        for i in videoesscreened:
            videoList.append(str(i['id']))
        listvideo = []
        listvideo = list(Video.objects.filter(Q(id__in=videoList)))
        groupsattended = json.loads(str(sheetdict['farmer_groups_targeted']))
        groupList=[]
        for i in groupsattended:
            groupList.append(str(i['id']))
        listgroup = []
        listgroup = list(PersonGroup.objects.filter(Q(id__in=groupList)))

        farmersattended = json.loads(str(sheetdict['farmers_attendance']))
        farmerList=[]
        for i in farmersattended:
            farmerList.append(str(i['person_id']))
        listfarmer = []
        listfarmer = list(Person.objects.filter(Q(id__in=farmerList)))
        ##Todo Category
        if sheetdict['online_id']=='':
            screeningObject = Screening(date=date,village=villageObject,animator=animatorObject,start_time=start_time,partner=partnerObject)
            screeningObject.save()
            for obj in listfarmer:
                PersonMeetingAttendance.objects.get_or_create(screening=screeningObject,person=obj)
            screeningObject.farmer_groups_targeted.add(*listgroup)
            screeningObject.videoes_screened.add(*listvideo)
        else:
            screeningObject = Screening.objects.get(id = sheetdict['online_id'])
            screeningObject.date = date
            screeningObject.village = villageObject
            screeningObject.animator = animatorObject
            screeningObject.start_time = start_time
            screeningObject.save()
            screeningObject.farmer_groups_targeted.add(*listgroup)
            screeningObject.videoes_screened.add(*listvideo)
            for obj in listfarmer:
                PersonMeetingAttendance.objects.get_or_create(screening=screeningObject,person=obj)


    data = []
    sheet = wb.sheet_by_name('adoption')
    rowcount = sheet.nrows
    colcount = sheet.ncols
    for row in range(1,rowcount):
        sheetdict= {}
        for col in range(0,colcount):
            key = sheet.cell(0,col).value
            value = sheet.cell(row,col).value
            if value =='null':
                value=None
            sheetdict[key] = value
        animator = json.loads(str(sheetdict['animator']))
        try:
            animatorObject = Animator.objects.get(id=animator['id'])
        except:
            animatorObject = None
        adopt_practice = sheetdict['adopt_practice']
        date_of_adoption = sheetdict['date_of_adoption']
        village = json.loads(str(sheetdict['village']))
        villageObject = Village.objects.get(id=village['id'])
        video = json.loads(str(sheetdict['video']))
        videoObject = Video.objects.get(id=video['id'])
        person = json.loads(str(sheetdict['person']))
        personObject = Person.objects.get(id=person['id'])
        if sheetdict['online_id']=='':
            adoptionObject = PersonAdoptPractice(person=personObject,video=videoObject,date_of_adoption=date_of_adoption,animator=animatorObject,adopt_practice=adopt_practice)
            adoptionObject.save()

        else:
            adoptionObject = PersonAdoptPractice.objects.get(id=sheetdict['online_id'])
            adoptionObject.person = personObject
            adoptionObject.video = videoObject
            adoptionObject.date_of_adoption = date_of_adoption
            adoptionObject.animator = animatorObject
            adoptionObject.adopt_practice = adopt_practice
            adoptionObject.save()