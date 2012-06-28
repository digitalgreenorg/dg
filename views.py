from django.shortcuts import *
from django.http import Http404, HttpResponse, QueryDict
from dashboard.models import *
from views import *
from forms import *
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render_to_response
from django.db import connection, transaction
from django.db.models import Q
from output.database.utility import run_query, run_query_dict
import datetime
import cjson
import re
from django.core import serializers
from django.contrib import auth

# autocomplete widget
import operator
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str
from django.conf.urls.defaults import *


def search(request):
    """
    Searches in the fields of the given related model and returns the
    result as a simple string to be used by the jQuery Autocomplete plugin
    """    
    query = request.GET.get('q', None)
    app_label = request.GET.get('app_label', None)
    model_name = request.GET.get('model_name', None)
    search_fields = request.GET.get('search_fields', None)

    if search_fields and app_label and model_name and query:
        def construct_search(field_name):
            # use different lookup methods depending on the notation
	    if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        model = models.get_model(app_label, model_name)
        qs = model._default_manager.all()
        for bit in query.split():
            or_queries = [models.Q(**{construct_search(
                    smart_str(field_name)): smart_str(bit)})
                    for field_name in search_fields.split(',')]
            other_qs = QuerySet(model)
            other_qs.dup_select_related(qs)
            other_qs = other_qs.filter(reduce(operator.or_, or_queries))
            qs = qs & other_qs
        data = ''.join([u'%s|%s\n' % (f.__unicode__(), f.pk) for f in qs])
        return HttpResponse(data)
    return HttpResponseNotFound()

def test(request, village_id):
    village = Village.objects.get(pk=int(village_id))
    animators = Animator.objects.filter(assigned_villages=village)
    json_subcat = serializers.serialize("json", animators)
    return HttpResponse("callback0(" + json_subcat + ");", mimetype="application/javascript")

def test_gwt(request, region_id):
    if request.method == 'POST':
        form = RegionTestForm(request.POST)
        if form.is_valid():
            new_form  = form.save(commit=False)
            new_form.id = request.POST['id']
            new_form.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Failure")
    else:
        return HttpResponse("Get Request")

def feed_animators(request, village_id):
    village = Village.objects.get(pk=int(village_id))
    animators = Animator.objects.filter(assigned_villages=village)
    json_subcat = serializers.serialize("json", animators)
    return HttpResponse(json_subcat, mimetype="application/javascript")

def feeds_persons(request, group_id):
    group = PersonGroups.objects.get(pk=int(group_id))
    persons = Person.objects.filter(group=group)
    json_subcat = serializers.serialize("json", persons)
    return HttpResponse(json_subcat, mimetype="application/javascript")


#Takes 'mode' parameter
#On mode = 0 , returns only list of persons and tot_val (value of TOTAL FORM in "Screening" page)
#On mode = 1, returns prac_list, persons and tot_val
def feed_person_html_on_person_group(request):
    mode = int(request.GET.get('mode'))
    group_id = request.GET.getlist('groups')
    init_id = request.GET.get('init')

    if(not(group_id and init_id) or mode not in [0,1]):
        return HttpResponse('{"html":\'Error\'}')

    all_persons = Person.objects.all()
    persons = []
    if group_id[0]:
        persons = Person.objects.all().filter(group__in = (PersonGroups.objects.all().filter(pk__in = group_id)))


    html = get_template('feeds/screening_view_person.txt')
    chomp = re.compile('\r|\n|\t')

    if(mode==0):
        return HttpResponse(cjson.encode(dict(tot_val=str(len(persons)+int(init_id)), \
                                                         html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
                                                         prac = chomp.sub('',get_prac()))))
    elif(mode==1):
        return HttpResponse(cjson.encode(dict(tot_val=str(len(persons)+int(init_id)), \
                                                         html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
                                                         prac = chomp.sub('',get_prac()))))


#Takes 'mode' parameter
#On mode = 0 , returns only list of persons and tot_val (value of TOTAL FORM in "Screening" page)
#On mode = 1, returns prac_list, persons and tot_val
# This function is different from the previous function in only one way, It uses a different get_template
def feed_person_html_on_person_group_modified(request):
    mode = int(request.GET.get('mode'))
    group_id = request.GET.getlist('groups')
    init_id = request.GET.get('init')

    if(not(group_id and init_id) or mode not in [0,1]):
        return HttpResponse('{"html":\'Error\'}')

    persons = []
    if group_id[0]:
        persons = Person.objects.all().filter(group__pk__in = group_id)


    html = get_template('feeds/screening_view_person_modified.txt')
    chomp = re.compile('\r|\n|\t')

    if(mode==0):
        return HttpResponse(cjson.encode(dict(tot_val=str(len(persons)+int(init_id)), \
                                                         html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
                                                         prac = chomp.sub('',get_prac()))))
    elif(mode==1):
        return HttpResponse(cjson.encode(dict(tot_val=str(len(persons)+int(init_id)), \
                                                         html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
                                                         prac = chomp.sub('',get_prac()))))


#return Practices in Options <options ..>...</option>
def get_prac():
    pracs = Practices.objects.all().order_by('practice_name')
    prac_list = Template("""{% for p in practices %}<option value="{{p.id}}">{{p.practice_name}}</option>{% endfor %}""")
    return prac_list.render(Context(dict(practices=pracs)))

# requires a person group or list of person groups.
def get_person(request):
    groups = request.GET.getlist('groups')
    persongroups = PersonGroups.objects.filter(id__in = groups)
    villages = Village.objects.none()
    for persongroup in persongroups:
        villages = villages | Village.objects.filter(id = persongroup.village.id)
    blocks = Block.objects.none()
    for village in villages:
        blocks = blocks | Block.objects.filter(id = village.block.id)
    p = Person.objects.all().filter(village__block__in = blocks).order_by('person_name')
    per_list = Template("""{% for p in per %}<option value="{{p.id}}">{{p.person_name}}{% if p.father_name %} ({{p.father_name}}){% endif %} ({{p.village}})</option>{% endfor %}""")
    return HttpResponse(cjson.encode(dict(per_list=per_list.render(Context(dict(per=p))))))


# Takes 'mode' argument
# mode : 0 Return only Practice_list
# mode : 2 Returns animator_list, persongroup_list, person_list, practice_list (requires 'vil_id')
def feed_person_prac_pg_anim(request):
    mode = int(request.GET.get('mode'))
    if(mode!=1): prac = get_prac()
    if(mode==0): return HttpResponse(cjson.encode(dict(prac_list=prac)))
    if 'vil_id' in request.GET:
        vil_id=int(request.GET.get('vil_id'))
        village = Village.objects.select_related(depth=1).get(id=int(vil_id))
        anim = serializers.serialize("json", Animator.objects.filter(assigned_villages=village))
        pg = serializers.serialize("json", PersonGroups.objects.filter(village=village))
        p = Person.objects.all().filter(village__block = village.block).order_by('person_name')
        per_list = Template("""{% for p in per %}<option value="{{p.id}}">{{p.person_name}} ({{p.village}})</option>{% endfor %}""")
        if(mode==1):
            return HttpResponse(cjson.encode(dict(per_list=per_list.render(Context(dict(per=p))),anim=anim,pg=pg)))
        elif(mode==2):
            return HttpResponse(cjson.encode(dict(prac_list=prac,per_list=per_list.render(Context(dict(per=p))),anim=anim,pg=pg)))

    return HttpResponse('')


def feeds_persons_village(request, village_id):
    village = Village.objects.get(pk=int(village_id))
    persons = Person.objects.filter(village=village_id)
    json_subcat = serializers.serialize("json", persons)
    return HttpResponse(json_subcat, mimetype="application/javascript")

#
#  Functions for online offline application
#
def redirect_url(request):
    return HttpResponseRedirect('/coco/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            #auth.login(request, user)
            request.session['username'] = user.username
            request.session['user_id'] = user.id
            user = UserPermission.objects.filter(username=user.id)
            return HttpResponse(user[0].role)
        else:
            # Show an error page
            return HttpResponse("0")
    else:
        return HttpResponse("error")

def get_key_for_user(request):
    if request.method == 'POST':
        BILLION_CONSTANT = 1000000000
        username = request.POST.get('username', '')
        user_id = run_query("Select id from auth_user where username = %s", username)
        if len(user_id) > 0 :
            result = run_query("Select id from user where user_id = %s", user_id[0].get('id'))
            if len(result) == 0:
                query_string = "insert into user(id, user_id) values (%s, %s)"
                id = (int (user_id[0].get('id')) * BILLION_CONSTANT) + 1000
                query_args = [id, user_id[0].get('id')]
                cursor = connection.cursor()
                cursor.execute(query_string, query_args)
                transaction.commit_unless_managed()
                id_str = id
            else:
                id_str = result[0].get('id')
        else:
            return HttpResponse("0")
        districts = get_user_districts(request)
        dict = {
            'dashboard_error_count': Error.objects.filter(district__in =  districts).filter(notanerror=0).count(),
            'last_id' : id_str
        }
        return HttpResponse(cjson.encode(dict), status=201)
    else:
        return HttpResponse("error")

def set_key_for_user(request):
    if request.method =='POST':
        user_id = run_query("Select id from auth_user where username = %s", request.POST.get('username', ''))
        if len(user_id) > 0:
            sql_query = "update user set id=%s where user_id =%s"
            query_args = [request.POST.get('id', ''), user_id[0].get('id')]
            cursor = connection.cursor()
            cursor.execute(sql_query ,query_args)
            transaction.commit_unless_managed()
            return HttpResponse("synced")
        else:
            return HttpResponse("0")

def get_user_villages(request):
    user_permissions = UserPermission.objects.filter(username = request.session.get('user_id'))
    villages = Village.objects.none()
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            villages = villages | Village.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
            districts = District.objects.filter(state__in = states)
            blocks = Block.objects.filter(district__in = districts)
            villages = villages | Village.objects.filter(block__in = blocks)
        if(user_permission.role=='F'):
            blocks = Block.objects.filter(district = user_permission.district_operated)
            villages = villages | Village.objects.filter(block__in = blocks)
    return villages

def get_user_blocks(request):
    user_permissions = UserPermission.objects.filter(username = request.session.get('user_id'))
    blocks = Block.objects.none()
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            blocks = blocks | Block.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
            districts = District.objects.filter(state__in = states)
            blocks = blocks | Block.objects.filter(district__in = districts)
        if(user_permission.role=='F'):
            blocks = blocks | Block.objects.filter(district = user_permission.district_operated)
    return blocks



def get_user_districts(request):
    user_permissions = UserPermission.objects.filter(username = request.session.get('user_id'))
    districts = District.objects.none()
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            districts = districts | District.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
            districts = districts | District.objects.filter(state__in = states)
        if(user_permission.role=='F'):
            districts = districts | District.objects.filter(district_name = user_permission.district_operated)
    return districts

def get_user_states(request):
    user_permissions = UserPermission.objects.filter(username = request.session.get('user_id'))
    states = State.objects.none()
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            states = State.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
        if(user_permission.role=='F'):
            states = State.objects.filter(district__district_name = user_permission.district_operated)
    return states

def save_country_online(request,id):
    if request.method == 'POST':
        if(id):
            country = Country.objects.get(id = id)
            form = CountryForm(request.POST, instance = country)
        else:
            form  = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            country = Country.objects.get(id = id)
            form = CountryForm(instance = country)
        else:
            form  = CountryForm()
        return HttpResponse(form)

def get_countries_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('country')
    else:
        countries = Country.objects.order_by("-id")[offset:limit]
        count = Country.objects.count()
        if(countries):
            json_subcat = serializers.serialize("json", countries)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response


def save_country_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = CountryForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            country = Country.objects.get(id=id)
            form = CountryForm(request.POST, instance = country)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_region_online(request,id):
    if request.method == 'POST':
        if(id):
            region = Region.objects.get(id = id)
            form = RegionForm(request.POST, instance = region)
        else:
            form  = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            region = Region.objects.get(id = id)
            form = RegionForm(instance = region)
        else:
            form  = RegionForm()
        return HttpResponse(form)

def get_regions_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('region')
    else:
        regions = Region.objects.order_by("-id")[offset:limit]
        count = Region.objects.count()
        if(regions):
            json_subcat = serializers.serialize("json", regions)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response


def save_region_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = RegionForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            region = Region.objects.get(id=id)
            form = RegionForm(request.POST, instance = region)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_state_online(request,id):
    if request.method == 'POST':
        if(id):
            state = State.objects.get(id = id)
            form = StateForm(request.POST, instance = state)
        else:
            form  = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            state = State.objects.get(id = id)
            form = StateForm(instance = state)
        else:
            form  = StateForm()
        return HttpResponse(form)

def get_states_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('states')
    else:
        states = State.objects.select_related('region','country').order_by("-id")[offset:limit]
        count = State.objects.select_related('region','country').count()
        if(states):
            json_subcat = serializers.serialize("json", states,  relations=('region','country'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_state_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = StateForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            state = State.objects.get(id=id)
            form = StateForm(request.POST, instance = state)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_fieldofficer_online(request,id):
    if request.method == 'POST':
        if(id):
            fieldofficer = FieldOfficer.objects.get(id = id)
            form = FieldOfficerForm(request.POST, instance = fieldofficer)
        else:
            form  = FieldOfficerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            fieldofficer = FieldOfficer.objects.get(id = id)
            form = FieldOfficerForm(instance = fieldofficer)
        else:
            form  = FieldOfficerForm()
        return HttpResponse(form)


def get_fieldofficers_online(request, offset, limit ):
    if request.method == 'POST':
        return redirect('fieldofficer')
    else:
        count = FieldOfficer.objects.count()
        fieldofficers = FieldOfficer.objects.order_by("-id")[offset:limit]
        if(fieldofficers):
            json_subcat = serializers.serialize("json", fieldofficers)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_fieldofficer_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = FieldOfficerForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            fieldofficer = FieldOfficer.objects.get(id=id)
            form = FieldOfficerForm(request.POST, instance = fieldofficer)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_practice_online(request,id):
    if request.method == 'POST':
        if(id):
            practice = Practices.objects.get(id = id)
            form = PracticeForm(request.POST, instance = practice)
        else:
            form  = PracticeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            practice = Practices.objects.get(id = id)
            form = PracticeForm(instance = practice)
        else:
            form  = PracticeForm()
        return HttpResponse(form)

def get_practices_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('practice')
    else:
        searchText = request.GET.get('searchText')
        count = Practices.objects.count()
        if(searchText):
            count = Practices.objects.filter(Q(practice_name__icontains = searchText)).count()
            practices = Practices.objects.filter(Q(practice_name__icontains = searchText)).order_by("practice_name")[offset:limit]
        else:
             practices = Practices.objects.order_by("-id")[offset:limit]
        if(practices):
            json_subcat = serializers.serialize("json", practices)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_practice_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PracticeForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            practice = Practices.objects.get(id=id)
            form = PracticeForm(request.POST, instance = practice)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def get_practices_seen_for_person(request, person_id):
    practices = Person.objects.get(pk=person_id).screening_set.values_list('videoes_screened__related_agricultural_practices', 
                                                    'videoes_screened__related_agricultural_practices__practice_name').distinct()                                                    
    html_template = """
    <option value='' selected='selected'>---------</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=practices)))
    
    return HttpResponse(html)

def save_language_online(request,id):
    if request.method == 'POST':
        if(id):
            language = Language.objects.get(id = id)
            form = LanguageForm(request.POST, instance = language)
        else:
            form  = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            language = Language.objects.get(id = id)
            form = LanguageForm(instance = language)
        else:
            form  = LanguageForm()
        return HttpResponse(form)

def get_languages_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('language')
    else:
        count = Language.objects.count()
        languages = Language.objects.order_by("-id")[offset:limit]
        if(languages):
            json_subcat = serializers.serialize("json", languages)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_language_offline(request,id):
    if request.method == 'POST':
        if(not id):
            form = LanguageForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            language = Language.objects.get(id=id)
            form = LanguageForm(request.POST, instance = language)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_partner_online(request,id):
    if request.method == 'POST':
        if(id):
            partner = Partners.objects.get(id = id)
            form = PartnerForm(request.POST, instance = partner)
        else:
            form  = PartnerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            partner = Partners.objects.get(id = id)
            form = PartnerForm(instance = partner)
        else:
            form  = PartnerForm()
        return HttpResponse(form)

def get_partners_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('partner')
    else:
        count = Partners.objects.count()
        partners = Partners.objects.order_by("-id")[offset:limit]
        if(partners):
            json_subcat = serializers.serialize("json", partners)
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_partner_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PartnerForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            partner = Partners.objects.get(id=id)
            form = PartnerForm(request.POST, instance = partner)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_video_online(request,id):
    if request.method == 'POST':
        if(id):
            video = Video.objects.get(id = id)
            form = VideoForm(request.POST, instance = video)
        else:
            form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        if(id):
            video = Video.objects.get(id = id)
            form = VideoForm(instance = video)
        else:
            form = VideoForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        form.fields['facilitator'].queryset = Animator.objects.filter(assigned_villages__in = villages).distinct().order_by('name')
        form.fields['cameraoperator'].queryset = Animator.objects.filter(assigned_villages__in = villages).distinct().order_by('name')
        form.fields['related_agricultural_practices'].queryset = Practices.objects.distinct().order_by('practice_name')
        form.fields['farmers_shown'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
        form.fields['supplementary_video_produced'].queryset = Video.objects.filter(village__in = villages).distinct().order_by('title')
        return HttpResponse(form)

def get_videos_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('video')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        videos_seen = set(Person.objects.filter(village__in = villages).values_list('screening__videoes_screened', flat=True))
        videos = Video.objects.filter(Q(village__in = villages) | Q(id__in = videos_seen)).distinct()
        if(searchText):
            vil = villages.filter(village_name__icontains = searchText)         
            videos_text = videos.filter( Q(id__icontains = searchText) | Q(title__icontains = searchText) | Q(village__in = vil))
            video_with_prod_start_date = video_with_prod_start_month = video_with_prod_start_year = Video.objects.none()
            video_with_prod_end_date = video_with_prod_end_month = video_with_prod_end_year = Video.objects.none()
            try: 
                video_with_prod_start_date = videos.filter(Q(video_production_start_date=searchText))
            except ValidationError:
                pass
            try:
                video_with_prod_start_month = videos.filter(Q(video_production_start_date__month=searchText))
            except ValueError:
                pass
            try:
                video_with_prod_start_year = videos.filter(Q(video_production_start_date__year=searchText))
            except ValueError:
                pass
            try:
                video_with_prod_end_date = videos.filter(Q(video_production_end_date=searchText))
            except ValidationError:
                pass 
            try:
                video_with_prod_end_month = videos.filter(Q(video_production_end_date__month=searchText))
            except ValueError:
                pass
            try:
                video_with_prod_end_year = videos.filter(Q(video_production_end_date__year=searchText))
            except ValueError:
                pass
            videos = videos_text | video_with_prod_start_date | video_with_prod_start_month | video_with_prod_start_year | video_with_prod_end_date | video_with_prod_end_month | video_with_prod_end_year
            videos = videos.distinct().order_by("-id")
        count = videos.count()
        videos = videos[offset:limit]
        if(videos):
            json_subcat = serializers.serialize("json", videos, relations=('village',))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def get_videos_seen_for_person(request, person_id):    
    videos = Person.objects.filter(pk=person_id).values_list('screening__videoes_screened__id', 'screening__videoes_screened__title').distinct()
    html_template = """   <option value='' selected='selected'>---------</option>
        {% for row in rows %}<option value="{{row.0}}">{{row.1}}</option>{%endfor%}
        """    
    t = Template(html_template);
    html = t.render(Context(dict(rows=videos)))
    
    return HttpResponse(html)

def save_video_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = VideoForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            video = Video.objects.get(id=id)
            form = VideoForm(request.POST, instance = video)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_videoagriculturalpractices_online(request,id):
    if request.method == 'POST':
        if(id):
            videoagriculturalpractices = VideoAgriculturalPractices.objects.get(id = id)
            form = VideoAgriculturalPracticesForm(request.POST, instance = videoagriculturalpractices)
        else:
            form = VideoAgriculturalPracticesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        if(id):
            videoagriculturalpractices = VideoAgriculturalPractices.objects.get(id = id)
            form = VideoAgriculturalPracticesForm(instance = videoagriculturalpractices)
        else:
            form = VideoAgriculturalPracticesForm()
        villages = get_user_villages(request)
        form.fields['video'].queryset = Video.objects.filter(village__in = villages).distinct().order_by('title')
        form.fields['practice'].queryset = Practices.objects.distinct().order_by('practice_name')
        return HttpResponse(form)

def get_videoagriculturalpractices_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('videoagriculturalpractices')
    else:
        villages = get_user_villages(request)
        videos = Video.objects.filter(village__in = villages).distinct().order_by("-id")
        videoagriculturalpractices = VideoAgriculturalPractices.objects.filter(video__in = videos).distinct().order_by("-id")[offset:limit]
        if(videoagriculturalpractices):
            json_subcat = serializers.serialize("json", videoagriculturalpractices)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_videoagriculturalpractices_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = VideoAgriculturalPracticesForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            videoagriculturalpractice = VideoAgriculturalPractices.objects.get(id=id)
            form = VideoAgriculturalPracticesForm(request.POST, instance = videoagriculturalpractice)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_personshowninvideo_online(request,id):
    if request.method == 'POST':
        if(id):
            personshowninvideo = PersonShownInVideo.objects.get(id = id)
            form = PersonShownInVideoForm(request.POST, instance = personshowninvideo)
        else:
            form = PersonShownInVideoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        if(id):
            personshowninvideo = PersonShownInVideo.objects.get(id = id)
            form = PersonShownInVideoForm(instance = personshowninvideo)
        else:
            form = PersonShownInVideoForm()
        villages = get_user_villages(request)
        form.fields['video'].queryset = Video.objects.filter(village__in = villages).distinct().order_by('title')
        form.fields['person'].queryset = Person.objects.distinct().order_by('person_name')
        return HttpResponse(form)

def get_personshowninvideo_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('personshowninvideo')
    else:
        villages = get_user_villages(request)
        videos = Video.objects.filter(village__in = villages).distinct().order_by("-id")
        personshowninvideo = PersonShownInVideo.objects.filter(video__in = videos).distinct().order_by("-id")[offset:limit]
        if(personshowninvideo):
            json_subcat = serializers.serialize("json", personshowninvideo)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_personshowninvideo_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonShownInVideoForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            personshowninvideo = PersonShownInVideo.objects.get(id=id)
            form = PersonShownInVideoForm(request.POST, instance = personshowninvideo)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_district_online(request,id):
    if request.method == 'POST':
        if(id):
            district = District.objects.get(id = id)
            form = DistrictForm(request.POST, instance = district)
        else:
            form  = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            district = District.objects.get(id = id)
            form = DistrictForm(instance = district)
        else:
            form  = DistrictForm()
        return HttpResponse(form)

def get_districts_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('districts')
    else:
        district_objects = get_user_districts(request)
        count = District.objects.filter(id__in = district_objects).distinct().count()
        districts = District.objects.filter(id__in = district_objects).distinct().order_by("-id")[offset:limit]
        if(districts):
            json_subcat = serializers.serialize("json", districts,  relations=('state','fieldofficer', 'partner'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_district_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = DistrictForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            district = District.objects.get(id=id)
            form = DistrictForm(request.POST, instance = district)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_block_online(request,id):
    if request.method == 'POST':
        if(id):
            block = Block.objects.get(id = id)
            form = BlockForm(request.POST, instance = block)
        else:
            form  = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            block = Block.objects.get(id = id)
            form = BlockForm(instance = block)
        else:
            form = BlockForm()
        districts = get_user_districts(request)
        form.fields['district'].queryset = districts.order_by('district_name')
        return HttpResponse(form)

def get_blocks_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('blocks')
    else:
        searchText = request.GET.get('searchText')
        districts = get_user_districts(request)
        count = Block.objects.filter(district__in = districts).distinct().count()
        if(searchText):
            dist = District.objects.filter(district_name__icontains = searchText)
            blocks = Block.objects.filter(district__in = districts)
            count = blocks.filter(Q(block_name__icontains = searchText) | Q(district__in = dist)).count()
            blocks = blocks.filter(Q(block_name__icontains = searchText) | Q(district__in = dist)).order_by("block_name")[offset:limit]
        else:
             blocks = Block.objects.filter(district__in = districts).distinct().order_by("-id")[offset:limit]
        if(blocks):
            json_subcat = serializers.serialize("json", blocks, relations=('district'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response
    
def get_blocks_for_district_online(request, district_id):
    blocks = Block.objects.filter(district__id = district_id).values_list('id', 'block_name').order_by("block_name")
                                                    
    html_template = """
    <option value='' selected='selected'>---------</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=blocks)))
    
    return HttpResponse(html)

def save_block_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = BlockForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            block = Block.objects.get(id=id)
            form = BlockForm(request.POST, instance = block)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_developmentmanager_online(request,id):
    if request.method == 'POST':
        if(id):
            developmentmanager = DevelopmentManager.objects.get(id = id)
            form = DevelopmentManagerForm(request.POST, instance = developmentmanager)
        else:
            form  = DevelopmentManagerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            developmentmanager = DevelopmentManager.objects.get(id = id)
            form = DevelopmentManagerForm(instance = developmentmanager)
        else:
            form  = DevelopmentManagerForm()
        return HttpResponse(form)

def get_developmentmanagers_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('developmentmanagers')
    else:
        count = DevelopmentManager.objects.select_related('region').count()
        developmentmanagers = DevelopmentManager.objects.select_related('region').order_by("-id")[offset:limit]
        if(developmentmanagers):
            json_subcat = serializers.serialize("json", developmentmanagers,  relations=('region',))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_developmentmanager_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = DevelopmentManagerForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            developmentmanager = DevelopmentManager.objects.get(id=id)
            form = DevelopmentManagerForm(request.POST, instance = developmentmanager)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_equipment_online(request,id):
    if request.method == 'POST':
        if(id):
            equipment = Equipment.objects.get(id = id)
            form = EquipmentForm(request.POST, instance = equipment)
        else:
            form  = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            equipment = Equipment.objects.get(id = id)
            form = EquipmentForm(instance = equipment)
        else:
            form  = EquipmentForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        
        return HttpResponse(form)


def get_equipments_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('equipments')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        count = Equipment.objects.filter(Q(village__in = villages) | Q(village__isnull = True)).count()
        equipments = Equipment.objects.filter(Q(village__in = villages) | Q(village__isnull = True))
        if(searchText):
            vil = villages.filter(Q(village_name__icontains = searchText) )
            count = equipments.filter(Q(id__icontains = searchText)  | Q(procurement_date__icontains = searchText) | Q(village__in = vil) | \
                        Q(invoice_no__icontains = searchText) | Q(remarks__icontains = searchText) | Q(model_no__icontains = searchText)).count()
            equipments = equipments.filter(Q(id__icontains = searchText) | Q(procurement_date__icontains = searchText) | Q(village__in = vil) | \
                        Q(invoice_no__icontains = searchText) | Q(remarks__icontains = searchText) | Q(model_no__icontains = searchText)).order_by("-village__village_name")[offset:limit]
        else:
            equipments = Equipment.objects.filter(Q(village__in = villages) | Q(village__isnull = True)).order_by("-village__village_name")[offset:limit]
        if(equipments):
            json_subcat = serializers.serialize("json", equipments,  relations=('equipmentholder','village',))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_equipment_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = EquipmentForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            equipment = Equipment.objects.get(id=id)
            form = EquipmentForm(request.POST, instance = equipment)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_village_online(request, id):
    PersonGroupInlineFormSet = inlineformset_factory(Village, PersonGroups,extra=5)
    AnimatorInlineFormSet = inlineformset_factory(Village, Animator, exclude=('assigned_villages',), extra=5)
    if request.method == "POST":
        if(id):
            village = Village.objects.get(id=id)
            form = VillageForm(request.POST, instance = village)
            formset_person_group = PersonGroupInlineFormSet(request.POST, request.FILES, instance = village)
            formset_animator = AnimatorInlineFormSet(request.POST, request.FILES, instance = village)
        else:
            form = VillageForm(request.POST)
            formset_person_group = PersonGroupInlineFormSet(request.POST, request.FILES)
            formset_animator = AnimatorInlineFormSet(request.POST, request.FILES)
        if form.is_valid() and formset_person_group.is_valid() and formset_animator.is_valid():
            saved_village = form.save()
            village = Village.objects.get(pk=saved_village.id)
            formset_person_group = PersonGroupInlineFormSet(request.POST, request.FILES, instance=village)
            formset_animator = AnimatorInlineFormSet(request.POST, request.FILES, instance=village)
            formset_person_group.save()
            formset_animator.save()
            return HttpResponse('')
        else:
            errors = form.errors.as_text()
            for form_person_group in formset_person_group.forms:
                if(form_person_group.errors):
                    errors = errors + '\n' + form_person_group.errors.as_text()
            for form_animator in formset_animator.forms:
                if(form_animator.errors):
                    errors = errors + '\n' + form_animator.errors.as_text()
            return HttpResponse(errors, status=201)
    else:
        if(id):
            village = Village.objects.get(id=id)
            form = VillageForm(instance = village)
            formset_person_group = PersonGroupInlineFormSet(instance = village)
            formset_animator = AnimatorInlineFormSet(instance = village)
        else:
            form = VillageForm()
            formset_person_group = PersonGroupInlineFormSet()
            formset_animator = AnimatorInlineFormSet()
        blocks = get_user_blocks(request)
        form.fields['block'].queryset = blocks.order_by('block_name')
        form_list = list(form)
        return HttpResponse(form.as_table() + formset_person_group.as_table() + formset_animator.as_table())

def get_villages_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('villages')
    else:
        searchText = request.GET.get('searchText')
        village_objects = get_user_villages(request)
        blocks = get_user_blocks(request)
        count = Village.objects.filter(id__in = village_objects).distinct().count()
        villages = Village.objects.filter(id__in = village_objects).distinct()
        if(searchText):
            blocks = blocks.filter(block_name__icontains = searchText)
            count = villages.filter(Q(village_name__icontains = searchText) | Q(block__in = blocks)).count()
            villages = villages.filter(Q(village_name__icontains = searchText) | Q(block__in = blocks)).order_by("village_name")[offset:limit]
        else:
            villages = Village.objects.filter(id__in = village_objects).distinct().order_by("-id")[offset:limit]
        if(villages):
            json_subcat = serializers.serialize("json", villages,  relations=('block',))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def get_villages_for_blocks_online(request, block_id):
    villages = Village.objects.filter(block__id = block_id).values_list('id', 'village_name').order_by('village_name')
                                                    
    html_template = """
    <option value='' selected='selected'>---------</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=villages)))
    
    return HttpResponse(html)

def save_village_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = VillageForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            village = Village.objects.get(id=id)
            form = VillageForm(request.POST, instance = village)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_animator_online(request, id):
    AnimatorAssignedVillageInlineFormSet = inlineformset_factory(Animator, AnimatorAssignedVillage, extra=3)
    if request.method == "POST":
        if(id):
            animator = Animator.objects.get(pk=id)
            form_animator = AnimatorForm(request.POST,instance=animator)
            formset_animator_assigned_village = AnimatorAssignedVillageInlineFormSet(request.POST, request.FILES,instance = animator)
        else:
            form_animator = AnimatorForm(request.POST)
        if form_animator.is_valid():
            saved_animator = form_animator.save()
            animator = Animator.objects.get(pk=saved_animator.id)
            formset_animator_assigned_village = AnimatorAssignedVillageInlineFormSet(request.POST, request.FILES, instance=animator)
            if formset_animator_assigned_village.is_valid():
                formset_animator_assigned_village.save()
                return HttpResponse('')
            else:
                errors = form_animator.errors.as_text()
                for form_anim in formset_animator_assigned_village.forms:
                    if(form_anim.errors):
                        errors = errors + '\n' + form_anim.errors.as_text()
                return HttpResponse(errors, status=201)
        else:
            errors = form_animator.errors.as_text()
            return HttpResponse(errors, status=201)
    else:
        if(id):
            animator = Animator.objects.get(id=id)
            form = AnimatorForm(instance = animator)
            formset = AnimatorAssignedVillageInlineFormSet(instance = animator)
        else:
            form = AnimatorForm()
            formset = AnimatorAssignedVillageInlineFormSet()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        for f in formset.forms:
            f.fields['village'].queryset = villages.order_by('village_name')
        return HttpResponse(form.as_table() + formset.as_table())

def get_animators_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('animators')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        count = Animator.objects.filter(village__in = villages).distinct().count()
        animators = Animator.objects.filter(village__in = villages).distinct()
        if(searchText):
            vil = villages.filter(village_name__icontains = searchText)
            partners = Partners.objects.filter(partner_name__icontains = searchText)
            count = animators.filter(Q(village__in = vil) | Q(name__icontains = searchText) | Q(partner__in = partners)).count()
            animators = animators.filter(Q(village__in = vil) | Q(name__icontains = searchText) | Q(partner__in = partners)).distinct().order_by("name")[offset:limit]
        else:
            animators = Animator.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(animators):
            json_subcat = serializers.serialize("json", animators,  relations=('partner','village'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response


def save_animator_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = AnimatorForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            animator = Animator.objects.get(id=id)
            form = AnimatorForm(request.POST, instance = animator)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_animatorassignedvillage_online(request,id):
    if request.method == 'POST':
        if id:
            animatorassignedvillage = AnimatorAssignedVillage.objects.get(id=id)
            form = AnimatorAssignedVillageForm(request.POST, instance = animatorassignedvillage)
        else:
            form = AnimatorAssignedVillageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        if id:
            animatorassignedvillage = AnimatorAssignedVillage.objects.get(id=id)
            form = AnimatorAssignedVillageForm(instance = animatorassignedvillage)
        else:
            form = AnimatorAssignedVillageForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        form.fields['animator'].queryset = Animator.objects.filter(village__in = villages).distinct().order_by('name')
        return HttpResponse(form)

def get_animatorassignedvillages_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('animatorassignedvillages')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        count = AnimatorAssignedVillage.objects.filter(village__in = villages).distinct().count()
        animatorassignedvillages = AnimatorAssignedVillage.objects.filter(village__in = villages).distinct().order_by("-id")
        if(searchText):
            vil = villages.filter(village_name__icontains = searchText)
            animators = Animator.objects.filter(Q(village__in = villages) & Q(name__icontains = searchText))
            count = AnimatorAssignedVillage.objects.filter(Q(village__in = vil) | Q(animator__in = animators) ).count()
            animatorassignedvillages = animatorassignedvillages.filter(Q(village__in = vil) | Q(animator__in = animators) )\
            .order_by("animator__name")[offset:limit]
        else:
            animatorassignedvillages = AnimatorAssignedVillage.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(animatorassignedvillages):
            json_subcat = serializers.serialize("json", animatorassignedvillages,  relations=('animator','village'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response


def save_animatorassignedvillage_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = AnimatorAssignedVillageForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            return HttpResponse("0")
        else:
            animatorassignedvillage = AnimatorAssignedVillage.objects.get(id=id)
            form = AnimatorAssignedVillageForm(request.POST, instance = animatorassignedvillage)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            return HttpResponse("0")

def save_persongroup_online(request,id):
    PersonFormSet = inlineformset_factory(PersonGroups, Person,exclude=('relations','adopted_agricultural_practices',), extra=30)
    if request.method == 'POST':
        if(id):
            persongroup = PersonGroups.objects.get(id = id)
            form = PersonGroupsForm(request.POST, instance = persongroup)
            formset = PersonFormSet(request.POST, request.FILES, instance = persongroup)
        else:
            form = PersonGroupsForm(request.POST)
            formset = PersonFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            saved_persongroup = form.save()
            persongroup = PersonGroups.objects.get(pk=saved_persongroup.id)
            formset = PersonFormSet(request.POST, request.FILES, instance=persongroup)
            formset.save()
            return HttpResponse('')
        else:
            errors = form.errors.as_text()
            for form_person in formset.forms:
                if(form_person.errors):
                    errors = errors + '\n' + form_person.errors.as_text()
            return HttpResponse(errors, status=201)
    else:
        if(id):
            persongroup = PersonGroups.objects.get(id = id)
            form = PersonGroupsForm(instance = persongroup)
            formset = PersonFormSet(instance = persongroup)
        else:
            form = PersonGroupsForm()
            formset = PersonFormSet()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        for f in formset.forms:
            f.fields['village'].queryset = villages.order_by('village_name')
        return HttpResponse(form.as_table() + formset.as_table())

def get_persongroups_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('persongroups')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        count = PersonGroups.objects.filter(village__in = villages).distinct().count()
        persongroups = PersonGroups.objects.filter(village__in = villages)
        if(searchText):
            vil = villages.filter(village_name__icontains = searchText)
            count = persongroups.filter(Q(village__in = vil) | Q(group_name__icontains = searchText)).count()
            persongroups = persongroups.filter(Q(village__in = vil) | Q(group_name__icontains = searchText)).order_by("group_name")[offset:limit]
        else:
            persongroups = PersonGroups.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(persongroups):
            json_subcat = serializers.serialize("json", persongroups,  relations=('village'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def get_persongroups_for_village_online(request, village_id):
    person_groups = PersonGroups.objects.filter(village__id = village_id).values_list('id', 'group_name').order_by('group_name')
                                                    
    html_template = """
    <option value='' selected='selected'>---------</option><option value='null'>No Group</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=person_groups)))
    
    return HttpResponse(html)

def save_persongroup_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonGroupsForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            persongroup = PersonGroups.objects.get(id=id)
            form = PersonGroupsForm(request.POST, instance = persongroup)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_person_online(request, id):
    if request.method == 'POST':
        if(id):
            person = Person.objects.get(id = id)
            form = PersonForm(request.POST, instance = person)
        else:
            form = PersonForm(request.POST)
        if form.is_valid():
            saved_person = form.save()
            return HttpResponse('')
        else:
            errors = form.errors.as_text()
            return HttpResponse(errors, status=201)
    else:
        if(id):
            person = Person.objects.get(id=id)
            form = PersonForm(instance = person)
        else:
            form = PersonForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        form.fields['group'].queryset = PersonGroups.objects.filter(village__in = villages).distinct().order_by('group_name')
        return HttpResponse(form.as_table())

def get_persons_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('persons')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        count = Person.objects.filter(village__in = villages).distinct().count()
        persons = Person.objects.filter(village__in = villages)
        if(searchText):
            vil = villages.filter(village_name__icontains = searchText)
            personGroups = PersonGroups.objects.filter(Q(village__in = villages) & Q(group_name__icontains = searchText))
            count = persons.filter(Q(person_name__icontains = searchText) | Q(village__in = vil) | Q(group__in = personGroups) ).count()
            persons = persons.filter(Q(person_name__icontains = searchText) | Q(village__in = vil) | Q(group__in = personGroups) ).order_by("person_name")[offset:limit]
        else:
            persons = Person.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(persons):
            json_subcat = serializers.serialize("json", persons,  relations={'group':{'fields':('group_name')},
                                                                             'village':{'fields':('village_name')}
                                                                             })
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def get_person_for_village_and_no_person_group_online(request, village_id):
    persons = Person.objects.filter(village__id = village_id, group=None).values_list('id', 'person_name', 'father_name').order_by("person_name")
    html_template = """
    <option value='' selected='selected'>---------</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}{% if row.2 %} ({{row.2}}){% endif %}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=persons)))
    
    return HttpResponse(html)

def get_person_for_person_group_online(request, group_id):
    persons = Person.objects.filter(group__id=group_id).values_list('id', 'person_name', 'father_name').order_by("person_name")
    html_template = """
    <option value='' selected='selected'>---------</option>
    {% for row in rows %}<option value="{{row.0}}">{{row.1}}{% if row.2 %} ({{row.2}}){% endif %}</option>{%endfor%}
    """
    t = Template(html_template);
    html = t.render(Context(dict(rows=persons)))
    
    return HttpResponse(html)

def save_person_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            person = Person.objects.get(id=id)
            form = PersonForm(request.POST, instance = person)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_personadoptpractice_online(request,id):
    if request.method == 'POST':
        if id:
            personadoptpractice = PersonAdoptPractice.objects.get(id=id)
            form = PersonAdoptPracticeForm(request.POST, instance = personadoptpractice)
        else:
            form = PersonAdoptPracticeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            villages = get_user_villages(request)
            form.fields['person'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
            if('person' in request.POST and request.POST['person']):
                form.fields['video'].queryset = Video.objects.filter(id__in = Person.objects.get(pk=request.POST['person']).screening_set.values_list('videoes_screened'))
            else:
                form.fields['video'].quersy = Video.objects.none()
            return HttpResponse(cjson.encode({'form':form.as_table(), 'errors':form.errors.as_text()}), status=201)
    else:
        if id:
            personadoptpractice = PersonAdoptPractice.objects.get(id=id)
            form = PersonAdoptPracticeForm(instance = personadoptpractice)
            villages = get_user_villages(request)
            form.fields['person'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
            form.fields['video'].queryset = Video.objects.filter(id__in = Person.objects.get(pk=personadoptpractice.person_id).screening_set.values_list('videoes_screened'))
            return HttpResponse(form)
        else:
            districts = get_user_districts(request)
            template = """<select name="district" id="id_district"><option value='' selected='selected'>---------</option>
                           {% for district in districts %}<option value='{{district.id}}'>{{district.district_name}}</option>{%endfor%}"""
            t = Template(template);
            return HttpResponse(t.render(Context(dict(districts=districts))))

def get_personadoptpractices_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('personadoptpractices')
    else:
        searchText = request.GET.get('searchText')
        villages = get_user_villages(request)
        personadoptpractices = PersonAdoptPractice.objects.filter(person__village__in = villages).distinct().order_by("-id")
        if(searchText):
            persongroups = PersonGroups.objects.filter(village__in = villages).filter(group_name__icontains = searchText)
            vil = villages.filter(village_name__icontains = searchText)
            per = Person.objects.filter(village__in = villages).filter(Q(person_name__icontains = searchText) | Q(village__in = vil) | Q(group__in = persongroups) )                        
            videos = Video.objects.filter(title__icontains = searchText)
            personadoptpractices = personadoptpractices.filter(Q(person__in = per) | Q(video__in = videos)).order_by("-id")
            count = personadoptpractices.count()
            personadoptpractices = personadoptpractices[offset:limit]
        else:
            count = personadoptpractices.count()
            personadoptpractices = personadoptpractices[offset:limit]
        if(personadoptpractices):
            json_subcat = serializers.serialize("json", personadoptpractices,indent=4,relations={'video':{'fields':('title')},
                                                                                                 'person':{'relations':{'village':{'fields':('village_name')},
                                                                                                                        'group':{'fields':('group_name')}}, 
                                                                                                           'fields':('person_name','village','group')}
                                                                                                 })
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response


def save_personadoptpractice_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonAdoptPracticeForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            return HttpResponse("0")
        else:
            personadoptpractice = PersonAdoptPractice.objects.get(id=id)
            form = PersonAdoptPracticeForm(request.POST, instance = personadoptpractice)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            return HttpResponse("0")


def save_screening_online(request,id):
    results = {}
    PersonMeetingAttendanceInlineFormSet = inlineformset_factory(Screening, PersonMeetingAttendance, extra=1)
    if request.method == 'POST':
        try:
            if(id):
                screening = Screening.objects.get(id = id)
                form = ScreeningForm(request.POST, instance = screening)
                formset = PersonMeetingAttendanceInlineFormSet(request.POST, request.FILES, instance = screening)
            else:
                form = ScreeningForm(request.POST)
                formset = PersonMeetingAttendanceInlineFormSet(request.POST, request.FILES)
            if form.is_valid() and formset.is_valid():
                saved_screening = form.save()
                screening = Screening.objects.get(pk=saved_screening.id)
                formset = PersonMeetingAttendanceInlineFormSet(request.POST, request.FILES, instance=screening)
                formset.save()
                return HttpResponse('')
            else:
                errors = form.errors.as_text()
                for form_person_meeting_attendance in formset.forms:
                    if(form_person_meeting_attendance.errors):
                        errors = errors + '\n' + form_person_meeting_attendance.errors.as_text()
                results["errors"] = errors
        except Exception as ex:
            print ex
    # Get Request or Form Error
    if(id):
        screening = Screening.objects.get(id = id)
        form = ScreeningForm(instance = screening)
        formset = PersonMeetingAttendanceInlineFormSet(instance = screening)
        form.fields['animator'].queryset = Animator.objects.filter(assigned_villages=screening.village).distinct().order_by('name')
        form.fields['farmer_groups_targeted'].queryset = PersonGroups.objects.filter(village = screening.village).distinct().order_by('group_name')
    else:
        form = ScreeningForm()
        form.fields['animator'].queryset = Animator.objects.none()
        form.fields['farmer_groups_targeted'].queryset = PersonGroups.objects.none()
    if "village" in request.POST:
        village_id = request.POST["village"]
        try:
            village = Village.objects.get(id=village_id)
            form.fields['animator'].queryset = Animator.objects.filter(assigned_villages=village).distinct().order_by('name')
            form.fields['farmer_groups_targeted'].queryset = PersonGroups.objects.filter(village = village).distinct().order_by('group_name')
        except:
            pass
    villages = get_user_villages(request)
    states = get_user_states(request)
    form.fields['village'].queryset = villages.order_by('village_name')
    form.fields['fieldofficer'].queryset = FieldOfficer.objects.distinct().order_by('name')
    form.fields['videoes_screened'].queryset = Video.objects.filter(village__block__district__state__in = states).distinct().order_by('title')
    results["form"] = form.as_table()
    if "errors" in results:
        return HttpResponse(cjson.encode(results), status=201)
    return HttpResponse(cjson.encode(results))

def get_attendance(request, id):
	PersonMeetingAttendanceInlineFormSet = inlineformset_factory(Screening, PersonMeetingAttendance, form=PersonMeetingAttendanceForm, extra=0)
	screening = Screening.objects.get(id = id)
	formset = PersonMeetingAttendanceInlineFormSet(instance = screening)
	personInMeeting = screening.farmers_attendance.distinct().order_by('person_name')
	practices = Practices.objects.all().order_by('practice_name')
	for form_person_meeting_attendance in formset.forms:
		form_person_meeting_attendance.fields['person'].queryset = personInMeeting
		form_person_meeting_attendance.fields['expressed_interest_practice'].queryset = practices
		form_person_meeting_attendance.fields['expressed_adoption_practice'].queryset = practices
		form_person_meeting_attendance.fields['expressed_question_practice'].queryset = practices
	return render_to_response('feeds/attendance.html',{'formset':formset})

def get_screenings_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('screenings')
    searchText = request.GET.get('searchText')
    villages = get_user_villages(request)
    count = Screening.objects.filter(village__in = villages).distinct().count()
    screenings = Screening.objects.filter(village__in = villages)
    if(searchText):
        vil = villages.filter(village_name__icontains = searchText)
        screening_in_village=screenings.filter(Q(village__in = vil))
        screening_on_date = Screening.objects.none()
        screening_on_day = Screening.objects.none()
        screening_on_month = Screening.objects.none()
        screening_on_year = Screening.objects.none()
        try:
            screening_on_date=screenings.filter(Q(date=searchText))
        except ValidationError:
            pass
        try:
            screening_on_day=screenings.filter(Q(date__day=searchText))
        except ValueError:
            pass
        try:
            screening_on_month=screenings.filter(Q(date__month=searchText))
        except ValueError:
            pass
        try:
            screening_on_year=screenings.filter(Q(date__year=searchText))
        except ValueError:
            pass
        screenings = screening_in_village | screening_on_date | screening_on_day | screening_on_month | screening_on_year
        count = len(screenings)
        screenings = screenings.order_by("date")[offset:limit]
    else:
        screenings = screenings.order_by("-id")[offset:limit]
    if(screenings):
        json_subcat = serializers.serialize("json", screenings, relations=('village',))
    else:
        json_subcat = 'EOF'
    response = HttpResponse(json_subcat, mimetype="application/javascript")
    response['X-COUNT'] = count
    return response

def save_screening_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = ScreeningForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            screening = Screening.objects.get(id=id)
            form = ScreeningForm(request.POST, instance = screening)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_groupstargetedinscreening_online(request):
    if request.method == 'POST':
        form = GroupsTargetedInScreeningForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = GroupsTargetedInScreeningForm()
        villages = get_user_villages(request)
        form.fields['screening'].queryset = Screening.objects.filter(village__in = villages).distinct().order_by('date')
        form.fields['persongroups'].queryset = PersonGroup.objects.filter(village__in = villages).distinct().order_by('group_name')
        return HttpResponse(form)

def get_groupstargetedinscreening_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('groupstargetedinscreening')
    else:
        villages = get_user_villages(request)
        screenings = Screening.objects.filter(village__in = villages).distinct().order_by("-id")
        groupstargetedinscreening = GroupsTargetedInScreening.objects.filter(screening__in = screenings).distinct().order_by("-id")[offset:limit]
        if(groupstargetedinscreening):
            json_subcat = serializers.serialize("json", groupstargetedinscreening)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_groupstargetedinscreening_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = GroupsTargetedInScreeningForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            grouptargeted = GroupsTargetedInScreening.objects.get(id=id)
            form = GroupsTargetedInScreeningForm(request.POST, instance = grouptargeted)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_videosscreenedinscreening_online(request):
    if request.method == 'POST':
        form = VideosScreenedInScreeningForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = VideosScreenedInScreeningForm()
        villages = get_user_villages(request)
        form.fields['screening'].queryset = Screening.objects.filter(village__in = villages).distinct().order_by('date')
        form.fields['video'].queryset = Video.objects.filter(village__in = villages).distinct().order_by('title')
        return HttpResponse(form)


def get_videosscreenedinscreening_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('videosscreenedinscreening')
    else:
        villages = get_user_villages(request)
        screenings = Screening.objects.filter(village__in = villages).distinct().order_by("-id")
        videosscreenedinscreening = VideosScreenedInScreening.objects.filter(screening__in = screenings).distinct().order_by("-id")[offset:limit]
        if(videosscreenedinscreening):
            json_subcat = serializers.serialize("json", videosscreenedinscreening)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_videosscreenedinscreening_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = VideosScreenedInScreeningForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            videoscreened = VideosScreenedInScreening.objects.get(id=id)
            form = VideosScreenedInScreeningForm(request.POST, instance = videoscreened)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_training_online(request,id):
    if request.method == 'POST':
        if(id):
            training = Training.objects.get(id = id)
            form = TrainingForm(request.POST, instance = training)
        else:
            form  = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            training = Training.objects.get(id = id)
            form = TrainingForm(instance = training)
        else:
            form = TrainingForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        form.fields['animators_trained'].queryset = Animator.objects.filter(village__in = villages).distinct().order_by('name')
        return HttpResponse(form)

def get_trainings_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('training')
    else:
        villages = get_user_villages(request)
        count = Training.objects.filter(village__in = villages).distinct().count()
        trainings = Training.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(trainings):
            json_subcat = serializers.serialize("json", trainings, relations=('village'))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_training_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = TrainingForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            training = Training.objects.get(id=id)
            form = TrainingForm(request.POST, instance = training)
            if form.is_valid():
                form.save()
                #form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_traininganimatorstrained_online(request):
    if request.method == 'POST':
        form = TrainingAnimatorsTrainedForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = TrainingAnimatorsTrainedForm()
        villages = get_user_villages(request)
        form.fields['animator'].queryset = Animator.objects.filter(village__in = villages).distinct().order_by('name')
        return HttpResponse(form)


def get_traininganimatorstrained_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('TrainingAnimatorsTrained')
    else:
        villages = get_user_villages(request)
        trainings = Training.objects.filter(village__in = villages).distinct().order_by("-id")
        traininganimatorstrained = TrainingAnimatorsTrained.objects.filter(training__in = trainings).distinct().order_by("-id")[offset:limit]
        if(traininganimatorstrained):
            json_subcat = serializers.serialize("json", traininganimatorstrained)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_traininganimatorstrained_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = TrainingAnimatorsTrainedForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            traininganimatortrained = TrainingAnimatorsTrained.objects.get(id=id)
            form = TrainingAnimatorsTrainedForm(request.POST, instance = traininganimatortrained)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_monthlycostpervillage_online(request):
    if request.method == 'POST':
        form = MonthlyCostPerVillageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = MonthlyCostPerVillageForm()
        villages = get_user_villages(request)
        form.fields['village'].queryset = villages.order_by('village_name')
        return HttpResponse(form)

def get_monthlycostpervillages_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('monthlycostpervillage')
    else:
        villages = get_user_villages(request)
        monthlycostpervillages = MonthlyCostPerVillage.objects.filter(village__in = villages).distinct().order_by("-id")[offset:limit]
        if(monthlycostpervillages):
            json_subcat = serializers.serialize("json", monthlycostpervillages, relations=('village',))
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_monthlycostpervillage_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = MonthlyCostPerVillageForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            monthlycostpervillage = MonthlyCostPerVillage.objects.get(id=id)
            form = MonthlyCostPerVillageForm(request.POST, instance = monthlycostpervillage)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")



def save_personrelation_online(request):
    if request.method == 'POST':
        form = PersonRelationsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = PersonRelationsForm()
        villages = get_user_villages(request)
        form.fields['person'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
        form.fields['relative'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
        return HttpResponse(form)


def get_personrelations_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('personrelations')
    else:
        villages = get_user_villages(request)
        persons = Person.objects.filter(village__in = villages).distinct().order_by("-id")
        personrelations = PersonRelations.objects.filter(person__in = persons).distinct().order_by("-id")[offset:limit]
        if(personrelations):
            json_subcat = serializers.serialize("json", personrelations)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_personrelation_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonRelationsForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            personrelations = PersonRelations.objects.get(id=id)
            form = PersonRelationsForm(request.POST, instance = personrelations)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_animatorsalarypermonth_online(request):
    if request.method == 'POST':
        form = AnimatorSalaryPerMonthForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = AnimatorSalaryPerMonthForm()
        villages = get_user_villages(request)
        form.fields['animator'].queryset = Animator.objects.filter(village__in = villages).distinct().order_by('name')
        return HttpResponse(form)


def get_animatorsalarypermonths_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('animatorsalarypermonths')
    else:
        villages = get_user_villages(request)
        animators = Animator.objects.filter(village__in = villages).distinct().order_by("-id")
        animatorsalarypermonths = AnimatorSalaryPerMonth.objects.filter(animator__in = animators).distinct().order_by("-id")[offset:limit]
        if(animatorsalarypermonths):
            json_subcat = serializers.serialize("json", animatorsalarypermonths,  relations=('animator',))
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_animatorsalarypermonth_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = AnimatorSalaryPerMonthForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            animatorsalarypermonth = AnimatorSalaryPerMonth.objects.get(id=id)
            form = AnimatorSalaryPerMonthForm(request.POST, instance = animatorsalarypermonth)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_personmeetingattendance_online(request):
    if request.method == 'POST':
        form = PersonMeetingAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = PersonMeetingAttendanceForm()
        villages = get_user_villages(request)
        form.fields['screening'].queryset = Screening.objects.filter(village__in = villages).distinct().order_by('date')
        form.fields['person'].queryset = Person.objects.filter(village__in = villages).distinct().order_by('person_name')
        form.fields['expressed_interest_practice'].queryset = Practice.objects.all().distinct().order_by('practice_name')
        return HttpResponse(form)
    
def get_personmeetingattendances_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('personmeetingattendances')
    else:
        villages = get_user_villages(request)
        screenings = Screening.objects.filter(village__in = villages).distinct().order_by("-id")
        personmeetingattendances = PersonMeetingAttendance.objects.filter(screening__in = screenings).distinct().order_by("-id")[offset:limit]
        if(personmeetingattendances):
            json_subcat = serializers.serialize("json", personmeetingattendances)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_personmeetingattendance_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = PersonMeetingAttendanceForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            personmeetingattendance = PersonMeetingAttendance.objects.get(id=id)
            form = PersonMeetingAttendanceForm(request.POST, instance = personmeetingattendance)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_equipmentholder_online(request):
    if request.method == 'POST':
        form = EquipmentHolderForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = EquipmentHolderForm()
        return HttpResponse(form)

def get_equipmentholders_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('equipmentholders')
    else:
        equipmentholders = EquipmentHolder.objects.order_by("-id")[offset:limit]
        if(equipmentholders):
            json_subcat = serializers.serialize("json", equipmentholders)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_equipmentholder_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = EquipmentHolderForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            equipmentholder = EquipmentHolder.objects.get(id=id)
            form = EquipmentHolderForm(request.POST, instance = equipmentholder)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")


def save_reviewer_online(request):
    if request.method == 'POST':
        form = ReviewerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(), status=201)
    else:
        form = ReviewerForm()
        return HttpResponse(form)

def get_reviewers_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('reviewers')
    else:
        reviewers = Reviewer.objects.order_by("-id")[offset:limit]
        if(reviewers):
            json_subcat = serializers.serialize("json", reviewers)
        else:
            json_subcat = 'EOF'
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_reviewer_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = ReviewerForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            reviewer = Reviewer.objects.get(id=id)
            form = ReviewerForm(request.POST, instance = reviewer)
            if form.is_valid():
                form.save()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def save_target_online(request,id):
    if request.method == 'POST':
        obj = QueryDict.__copy__(request.POST)
        month_year_year = request.POST.get('month_year_year')
        month_year_month = request.POST.get('month_year_month')
        if(month_year_year == "0") or (month_year_month == "0"):
            obj['month_year'] = ""
        else:
            obj['month_year'] = datetime.date(int(month_year_year), int(month_year_month), 1)
        if(id):
            target = Target.objects.get(id = id)
            form = TargetForm(obj, instance = target)
        else:
            form = TargetForm(obj)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponse(form.errors.as_text(),status = 201)
    else:
        if(id):
            target = Target.objects.get(id = id)
            form = TargetForm(instance = target)
        else:
            form = TargetForm()
        districts = get_user_districts(request)
        form.fields['district'].queryset = districts.order_by('district_name')
        return HttpResponse(form)

def get_targets_online(request, offset, limit):
    if request.method == 'POST':
        return redirect('target')
    else:
        districts = get_user_districts(request)
        count = Target.objects.filter(district__in = districts).distinct().count()
        targets = Target.objects.filter(district__in = districts).distinct().order_by("-id")[offset:limit]
        if(targets):
            json_subcat = serializers.serialize("json", targets, relations=('district',))
        else:
            json_subcat = 'EOF'
        response = HttpResponse(json_subcat, mimetype="application/javascript")
        response['X-COUNT'] = count
        return response

def save_target_offline(request, id):
    if request.method == 'POST':
        if(not id):
            form = TargetForm(request.POST)
            if form.is_valid():
                new_form  = form.save(commit=False)
                new_form.id = request.POST['id']
                new_form.save()
                form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")
        else:
            target = Target.objects.get(id=id)
            form = TargetForm(request.POST, instance = target)
            if form.is_valid():
                form.save()
                #form.save_m2m()
                return HttpResponse("1")
            else:
                return HttpResponse("0")

def get_dashboard_errors_online(request, offset, limit):
    districts = get_user_districts(request)
    all_errors = Error.objects.filter(district__in =  districts).order_by('notanerror','rule')
    count = all_errors.count()
    errors = all_errors[offset:limit]
    if errors:
        json_subcat = serializers.serialize("json",errors,indent=4,relations={'rule':{'fields':('error_msg',)}, 'content_type1':{'fields':('name','model',)}, 'content_type2':{'fields':('name','model',)}})
    else:
        json_subcate = "EOF"
    
    response = HttpResponse(json_subcat, mimetype="application/javascript")
    response['X-COUNT'] = count
    return response

def mark_error_as_not_error(request, offset, limit):
    if request.method == "POST":
        errorids = request.POST.getlist('errorid')
        errorids = [int(x) for x in errorids]
        #Deselected ones
        districts = get_user_districts(request)
        all_errors = Error.objects.filter(district__in =  districts).order_by('notanerror','rule')
        for err in all_errors[offset:limit]:
            if(err.notanerror==1 and err.id not in errorids):
                err.notanerror = 0
                err.save()
        #Newly Selected ones
        Error.objects.filter(pk__in=errorids).exclude(notanerror=1).update(notanerror=1)
        
        return HttpResponse();

def index_template_data(request):
    return_val = {}
    
    districts = get_user_districts(request)
    countoferrors = Error.objects.filter(district__in =  districts).filter(notanerror=0).count()
    
    return_val['dashboard_error_count'] = str(countoferrors)
    
    return HttpResponse(cjson.encode(return_val))

def persons_in_screening(request, screening_id):
    # test url http://127.0.0.1:8000/dashboard/personsinscreening/6000001033/
    person_ids = []
    if request.method == "GET":
        try:
            person_list = PersonMeetingAttendance.objects.filter(screening=screening_id).distinct().order_by("person__father_name").order_by("person__person_name").values_list('person_id',flat=True)
            #per.order_by("person_name").order_by("father_name").
        except:
            # log error. Send error message.
            print "No screening id."
    return HttpResponse(cjson.encode(list(person_list)), mimetype='application/json')

def farmers_in_groups(request):
    # test url http://127.0.0.1:8000/dashboard/personsingroup/?groups=5000001001
    if request.method == "GET":
        persongroup_ids = request.GET.getlist('groups')
        person_ids = []
        for group_id in persongroup_ids:
            try:
                group = PersonGroups.objects.get(id=group_id)
            except:
                # log an error
                continue
            person_ids.extend(group.person_set.distinct().order_by('father_name').order_by('person_name').values_list('id',flat=True))
        #person_ids = list(set(person_ids))
        return HttpResponse(cjson.encode(person_ids), mimetype='application/json')

def screenings_in_village(request, village_id):
    # test url - 127.0.0.1:8000/dashboard/screeningsinvillage/6000009723/
    data = {}
    if request.method == 'GET':
        try:
            village = Village.objects.get(id=village_id)
            persons_in_village = village.person_set.all().order_by('father_name').order_by('person_name')
            data['person_list'] = [{'value':"", 'string':"---------"}]
            for person in persons_in_village:
                data['person_list'].append({'value':person.id, 'string':str(person)})
            data['video_list'] = []
            videos = village.screening_set.values_list('videoes_screened__id','videoes_screened__title').distinct()
            for video in videos:
                data['video_list'].append({'value':video[0], 'string':video[1]})
        except Exception as ex:
            data['person_list'] = []
            data['video_list'] = []
            # print ex - log Exception
            # return error response
        return HttpResponse(cjson.encode(data), mimetype='application/json') 

def practices_seen_by_farmer(request, person_id):
    # test url - 127.0.0.1:8000/dashboard/practicesforperson/5000001002/
    if request.method == 'GET':
        try:
            farmer = Person.objects.get(id=person_id)
            video_list = farmer.screening_set.values_list('videoes_screened__id', 'videoes_screened__title')
            #practice_list = farmer.screening_set.values('videoes_screened__related_agricultural_practices__id', 'videoes_screened__related_agricultural_practices__practice_name')
            video_list = list(set(video_list))
        except:
            video_list = []
            # log an error
            # send an error status message back, maybe not
        data = {}
        video_data = []
        for vid in video_list:
            video_data.append({'value':vid[0],'string':vid[1]})    
        data['video_list'] = video_data
        data['person_list'] = [{'value':farmer.id, 'string':str(farmer)}]
        return HttpResponse(cjson.encode(data), mimetype='application/json')

def filters_for_village (request, village_id):
    data = {}
    if request.method == 'GET':
        try:
            village = Village.objects.get(id=village_id)
            data['village'] = {'value': village.id, 'string' : village.village_name } 
            animators = Animator.objects.filter(assigned_villages=village).distinct().order_by('name')
            data['animators'] = []
            for anim in animators:
                data['animators'].append({'value':anim.id,'string':anim.name})
            groups = PersonGroups.objects.filter(village=village).distinct().order_by('group_name')
            data['groups'] = []
            for group in groups:
                data['groups'].append({'value':group.id,'string':group.group_name})
        except:
            pass
        return HttpResponse(cjson.encode(data), mimetype='application/json') 

def person_meeting_attendance_data(request, person_id, screening_id):
    # test url http://127.0.0.1:8000/dashboard/personmeetingattendance/6000001019/6000001033/
    data = {}
    if request.method == 'GET':
        try:
            farmer = Person.objects.get(id=person_id)
            try:
                pma = PersonMeetingAttendance.objects.filter(person=person_id).get(screening=screening_id)
            except MultipleObjectsReturned:
                pma = PersonMeetingAttendance.objects.filter(person=person_id).filter(screening=screening_id)[0]
            video_list = farmer.screening_set.values_list('videoes_screened__id', 'videoes_screened__title')
            video_list = list(set(video_list))
            video_data = []
            for video in video_list:
                video_data.append({'value':video[0],'string':video[1]})
            data = {
                'pma' : {'id':pma.id,'screening':pma.screening_id},
                'person_list' : [{'value':farmer.id, 'string':str(farmer)}],
                'video_list': video_data,
                'expressed_question_comment': pma.expressed_question,
                'interested' : pma.interested,
            }

            if pma.expressed_adoption_video:
                data['selected_expressed_adoption_video'] = {
                    'value': pma.expressed_adoption_video.id,
                    'string': pma.expressed_adoption_video.title
                }
        except Exception as ex:
            print ex
            # log error
        return HttpResponse(cjson.encode(data), mimetype='application/json')

def practices_in_videos(request):
    # test url http://127.0.0.1:8000/dashboard/practicesinvideos/?video=6000007313&video=6000008464
    if request.method == "GET":
        video_ids = request.GET.getlist('video')
        practice_ids = []
        for video_id in video_ids:
            try:
                video = Video.objects.get(id=video_id)
            except:
                # log an error
                continue
            practice_ids.extend(video.related_agricultural_practices.values_list('id',flat=True))
        practice_ids = list(set(practice_ids))
        return HttpResponse(cjson.encode(practice_ids), mimetype='application/json')

 
