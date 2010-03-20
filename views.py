from django.shortcuts import *
from django.http import Http404, HttpResponse
from dg.dashboard.models import *
from dg.views import *
from dg.forms import *
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render_to_response
from django.db import connection, transaction
from dg.output.database import run_query 
import datetime
import re
import json
#import cjson
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


def hello(request):
	return HttpResponse("Hello world")

def homepage(request):
	return HttpResponse("This is a home page")

def current_datetime(request):
	now = datetime.datetime.now()
	#t = get_template('current_datetime.html')
	##html = "<html><body>It is now %s. </body></html>" %now
	#html = t.render(Context({'current_date':now}))
	#return HttpResponse(html)
	return render_to_response('current_datetime.html',{'current_date':now})

def hours_ahead(reqest,offset):
	try:
		hour_offset = int(offset)
	except ValueError:
		raise Http404()
	next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
	#assert False
	#html = "<html><body>In %s hour(s), it will be %s.<body></html>" % (offset, dt)
	#return HttpResponse(html)
	return render_to_response('hours_ahead.html',locals())



def test(request, village_id):
        village = Village.objects.get(pk=int(village_id))
        animators = Animator.objects.filter(assigned_villages=village)
        #return render_to_response('feeds/animators.txt', {'animators':animators}, mimetype="text/plain")
        json_subcat = serializers.serialize("json", animators)
        return HttpResponse("callback0(" + json_subcat + ");", mimetype="application/javascript")


def test_gwt(request, region_id):
	if request.method == 'POST':
		form = RegionTestForm(request.POST)
		if form.is_valid():
			#new_form = form.save()
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
		#str = "test" + "\t" + "Model" + "\n" + "test1" + "\t" + "Model1";	
		#temp = cjson.encode(str)
		#return HttpResponse(temp, mimetype="text/plain")
        return render_to_response('feeds/animators.txt', {'animators':animators}, mimetype="text/plain")



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
		return HttpResponse('{"html":\'Error\'}');
	
	all_persons = Person.objects.all()
	persons = []
	if group_id[0]:
		persons = Person.objects.all().filter(group__in = \
											  (PersonGroups.objects.all().filter(pk__in = group_id)))
											  
		
	html = get_template('feeds/screening_view_person.txt')
	
	chomp = re.compile('\r|\n|\t')
	if(mode==0):
		return HttpResponse(json.dumps(dict(tot_val=str(len(persons)+int(init_id)), \
								 html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
								 prac = chomp.sub('',get_prac()))))
	elif(mode==1):
		return HttpResponse(json.dumps(dict(tot_val=str(len(persons)+int(init_id)), \
								 html = chomp.sub('',html.render(Context(dict(persons=persons,init=init_id)))), \
								 prac = chomp.sub('',get_prac()))))
		
	
#return Practices in Options <options ..>...</option>
def get_prac():
	pracs = Practices.objects.all()
	prac_list = Template("""{% for p in practices %}<option value="{{p.id}}">{{p.practice_name}}</option>{% endfor %}""")
	return prac_list.render(Context(dict(practices=pracs)))


# Takes 'mode' argument 
# mode : 0 Return only Practice_list
# mode : 1 Returns animator_list, persongroup_list, person_list (requires 'vil_id')
# mode : 2 Returns animator_list, persongroup_list, person_list, practice_list (requires 'vil_id')
def feed_person_prac_pg_anim(request):
	mode = int(request.GET.get('mode'));
	if(mode!=1): prac = get_prac();
	if(mode==0): return HttpResponse(json.dumps(dict(prac_list=prac))) 
	if 'vil_id' in request.GET:
		vil_id=int(request.GET.get('vil_id'))
		village = Village.objects.select_related(depth=1).get(id=int(vil_id))
		anim = serializers.serialize("json", Animator.objects.filter(assigned_villages=village))		
		pg = serializers.serialize("json", PersonGroups.objects.filter(village=village))		
		p = Person.objects.all().filter(village__block = village.block).order_by('person_name')
		per_list = Template("""{% for p in per %}<option value="{{p.id}}">{{p.person_name}} ({{p.village}})</option>{% endfor %}""")
		if(mode==1):
			return HttpResponse(json.dumps(dict(per_list=per_list.render(Context(dict(per=p))),anim=anim,pg=pg)))
		elif(mode==2):
			return HttpResponse(json.dumps(dict(prac_list=prac,per_list=per_list.render(Context(dict(per=p))),anim=anim,pg=pg)))
	
	return HttpResponse('')
		

def feeds_persons_village(request, village_id):
	village = Village.objects.get(pk=int(village_id))
	persons = Person.objects.filter(village=village_id)
	json_subcat = serializers.serialize("json", persons)
	return HttpResponse(json_subcat, mimetype="application/javascript")


def login_view(request):
    if request.method == 'POST':
	    username = request.POST.get('username', '')
	    password = request.POST.get('password', '')
	    user = auth.authenticate(username=username, password=password)
	    if user is not None and user.is_active:
	        # Correct password, and the user is marked "active"
	        auth.login(request, user)
	        return HttpResponse("1")
	    else:
	        # Show an error page
        	return HttpResponse("0")
    else:
	    return HttpResponse("error")

def get_key_for_user(request):
	if request.method == 'POST':
		MILLION_CONSTANT = 1000000
		username = request.POST.get('username', '')
		user_id = run_query("Select id from auth_user where username = %s", username)
		if len(user_id) > 0 :
			result = run_query("Select id from user where user_id = %s", user_id[0].get('id'));
			if len(result) == 0:
				query_string = "insert into user(id, user_id) values (%s, %s)"
				id = int (user_id[0].get('id')) * MILLION_CONSTANT
				query_args = [id, user_id[0].get('id')]
				cursor = connection.cursor()
				cursor.execute(query_string, query_args)
				transaction.commit_unless_managed()
				return HttpResponse(id)
			else:	
				return HttpResponse(result[0].get('id'))
		else:
			return HttpResponse("0")
	else:
		return HttpResponse("error")
	
	
def save_region(request):
	if request.method == 'POST':
		#print request.POST
		form = RegionForm(request.POST)
		if form.is_valid():	
			#print request.COOKIES["username"]
			# This should redirect to show region page
			form.save()
			#print "works"
			#return HttpResponse("1")
			return HttpResponseRedirect('/dashboard/getregions/')
		else:
			#print "error"
			return HttpResponse("0")	
		
def get_regions(request):
	if request.method == 'POST':
		# This should handle the region DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('region')
	else:
		regions = Region.objects.order_by("-id")
		#regions = Region.objects.get(region_name="Beacons100")
		print regions
		json_subcat = serializers.serialize("json", regions)
		return HttpResponse(json_subcat, mimetype="application/javascript")
		#return render_to_response('regions.html', {'regions': regions})
	
def save_fieldofficer(request):
    if request.method == 'POST':
    	print request.POST
        form = FieldOfficerForm(request.POST)
        if form.is_valid():
            form.save()
            #print request.COOKIES["username"]
            return HttpResponseRedirect('/dashboard/getfieldofficers/')
        else:
            return HttpResponse("0")

def get_fieldofficers(request):
    if request.method == 'POST':
        return redirect('fieldofficer')
    else:
        fieldofficers = FieldOfficer.objects.order_by("-id")
        print fieldofficers
        json_subcat = serializers.serialize("json", fieldofficers)
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_practice(request):
    if request.method == 'POST':
    	print "save if : hi"
        form = PracticeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/getpractices/')
        else:
    	    print "save else : hi"
            return HttpResponse("0")
        
def get_practices(request):
    if request.method == 'POST':
    	#print "get if : hi"
        return redirect('practice')
    else:
    	#print "get else : hi"
        practices = Practices.objects.order_by("-id")
        #print practices
        json_subcat = serializers.serialize("json", practices)
        #print "get else : after json"
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_language(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/getlanguages/')
        else:
            return HttpResponse("0")
        
def get_languages(request):
    if request.method == 'POST':
        return redirect('language')
    else:
        languages = Language.objects.order_by("-id")
        print languages
        json_subcat = serializers.serialize("json", languages)
        return HttpResponse(json_subcat, mimetype="application/javascript")

def save_partner(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/getpartners/')
        else:
            return HttpResponse("0")
        
def get_partners(request):
    if request.method == 'POST':
        return redirect('partner')
    else:
        partners = Partner.objects.order_by("-id")
        print partners
        json_subcat = serializers.serialize("json", partners)
        return HttpResponse(json_subcat, mimetype="application/javascript")

def add_language(request):
	if request.method == 'POST':
		if 'language_name' in request.POST:
			language = request.POST['language_name']
			lang_obj = Language(language_name=language)
			lang_obj.save()
			# This should redirect to the language view at the bottom since we're going to
			# a different page as a GET request
			#return HttpResponseRedirect(reverse('dg.views.language', args=(language,)))
			#return redirect('language')
			return HttpResponseRedirect('/dashboard/languages/'+language)
	else:
		return render_to_response('lang_inherit.html')

def language(request,language):
	if request.method == 'POST':
		# This should handle the language DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('language')
	else:
		languages = Language.objects.order_by("-id")
		#if language:
		return render_to_response('languages.html', {'languages': languages, 'language':language})


def add_region(request):
	if request.method == 'POST':
		#print request.POST
		form = RegionForm(request.POST)
		if form.is_valid():	
			# This should redirect to show region page
			form.save()
			return HttpResponseRedirect('/dashboard/regions/')
		else:
			return render_to_response('add_region.html',{'form':form})
	else:
		form = RegionForm()
		#from django.core import serializers
	        #json_subcat = serializers.serialize("json", form)
        	#return HttpResponse(json_subcat, mimetype="application/javascript")
                #temp = cjson.encode(form)
                #return HttpResponse(temp, mimetype="text/plain")
		#return HttpResponse(form)
		return render_to_response('add_region.html',{'form':form})


def region(request):
	if request.method == 'POST':
		# This should handle the region DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('region')
	else:
		regions = Region.objects.order_by("-id")
		return HttpResponse(regions)
		#return render_to_response('regions.html', {'regions': regions})


def add_state(request):
	if request.method == 'POST':
		form = StateForm(request.POST)
		if form.is_valid():	
			# This should redirect to show region page
			form.save()
			return HttpResponseRedirect('/dashboard/states/')
		else:
			return render_to_response('add_state.html',{'form':form})
	else:
		form = StateForm()
		#temp = cjson.encode(form)
		return HttpResponse(form);
		#json_subcat = serializers.serialize("json", form)
		#return HttpResponse(json_subcat, mimetype="application/javascript")
		#return render_to_response('add_state.html',{'form':form})


def state(request):
	if request.method == 'POST':
		# This should handle the region DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('state')
	else:
		states = State.objects.order_by("-id")
		return render_to_response('states.html', {'states': states})

def add_district(request):
	if request.method == 'POST':
		form = DistrictForm(request.POST)
		if form.is_valid():	
			# This should redirect to show region page
			form.save()
			return HttpResponseRedirect('/dashboard/districts/')
		else:
			return render_to_response('add_district.html',{'form':form})
	else:
		form = DistrictForm()
		return render_to_response('add_district.html',{'form':form})


def district(request):
	if request.method == 'POST':
		# This should handle the region DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('district')
	else:
		districts = District.objects.order_by("-id")
		return render_to_response('districts.html', {'districts': districts})



def add_block(request):
	if request.method == 'POST':
		form = BlockForm(request.POST)
		if form.is_valid():	
			# This should redirect to show region page
			form.save()
			return HttpResponseRedirect('/dashboard/blocks/')
		else:
			return render_to_response('add_block.html',{'form':form})
	else:
		form = BlockForm()
		return render_to_response('add_block.html',{'form':form})


def block(request):
	if request.method == 'POST':
		# This should handle the region DELETE request

		# Now redirect back to ourselves as a GET to re-render the page
		return redirect('block')
	else:
		blocks = Block.objects.order_by("-id")
		return render_to_response('blocks.html', {'blocks': blocks})




def add_person_group(request):
        PersonFormSet = inlineformset_factory(PersonGroups, Person,extra=3, exclude=('equipmentholder','relations','adopted_agricultural_practices',))

        if request.method == 'POST':
                form = PersonGroupsForm(request.POST)
                formset = PersonFormSet(request.POST, request.FILES)
                if form.is_valid():
        	        saved_persongroup = form.save()
                	persongroup = PersonGroups.objects.get(pk=saved_persongroup.id)
                	formset = PersonFormSet(request.POST, request.FILES, instance=persongroup)
			if formset.is_valid():
				personformset = formset.save(commit=False)
	                        return HttpResponseRedirect('/admin/dashboard/persongroups/')
			else:
                         	return render_to_response('add_person_group.html', {'form':form, 'formset':formset})

                else:
                        return render_to_response('add_person_group.html', {'form':form, 'formset':formset})
        else:
                form = PersonGroupsForm()
                formset = PersonFormSet()
                return render_to_response('add_person_group.html', {'form':form,'formset':formset})



def add_person_group_1(request):
	PersonFormSet = modelformset_factory(Person, extra=3, exclude=('equipmentholder','relations','adopted_agricultural_practices',))

	if request.method == 'POST':
		form = PersonGroupsForm(request.POST)
                formset = PersonFormSet(request.POST, request.FILES)
		if form.is_valid():
			for k,v in request.POST.items():
			        if k[:5] == 'form-':
	        	        	s = k.split('-')
					if s[1] != u'TOTAL_FORMS' and s[1] != u'INITIAL_FORMS' and s[2] == 'village':
						request.POST[k] = request.POST['village']
		               			'''i = s[1]
			       		        if i not in a and s[1] != u'TOTAL_FORMS' and s[1] != u'INITIAL_FORMS':
							print s[1]
                	       				a[i] = {s[2]: v}
			        	        elif s[1] != u'TOTAL_FORMS' and s[1] != u'INITIAL_FORMS':
							print s[1]
        		       		        	a[i].update({s[2]: v})

			for k,v in a.items():
				print v
			        #p = PersonForm(**v)
				print cd['group_name']
				p = PersonForm({'group':cd['group_name'] ,'village': v['village'], 'phone_no': v['phone_no'], 'father_name': v['father_name'], 'person_name': v['person_name'], 'address': v['address'], 'gender': v['gender'], 'age': v['age'], 'land_holdings': v['land_holdings'], 'id': v['id']})
				if p.is_valid():
				        p.save()
					return HttpResponseRedirect('/admin/dashboard/persongroups/')
				else:
					print 'false'
					return render_to_response('add_person_group.html', {'form':form, 'formset':formset})'''
			formset = PersonFormSet(request.POST, request.FILES)

		        if formset.is_valid():
				save_tuple = form.save()

				for k,v in request.POST.items():
				        if k[:5] == 'form-':
	        		        	s = k.split('-')
						if s[1] != u'TOTAL_FORMS' and s[1] != u'INITIAL_FORMS' and s[2] == 'group':
							request.POST[k] = save_tuple.id

				formset = PersonFormSet(request.POST, request.FILES)	
				if formset.is_valid():
	            			formset.save()
					return HttpResponseRedirect('/admin/dashboard/persongroups/')
			else:
				return render_to_response('add_person_group.html', {'form':form, 'formset':formset})
		else:
			return render_to_response('add_person_group.html', {'form':form, 'formset':formset})

	else:
		form = PersonGroupsForm()
		formset = PersonFormSet(queryset=PersonGroups.objects.none())
		return render_to_response('add_person_group.html', {'form':form,'formset':formset})
			
def person_group(request):
	if request.method == 'POST':
		return redirect('person_group')
	else:
		persongroups = PersonGroups.objects.order_by("-id")
		return render_to_response('blocks.html',{'persongroups':persongroups})

def add_development_manager(request):
        if request.method == 'POST':
                form = DevelopmentManagerForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/developmentmanagers/')
                else:
                        return render_to_response('add_dm.html',{'form':form})
        else:
                form = DevelopmentManagerForm()
                return render_to_response('add_dm.html',{'form':form})


def development_manager(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('development_manager')
        else:
                dms = DevelopmentManager.objects.order_by("-id")
                return render_to_response('dm.html', {'dms': dms})
 

def add_animator_assigned_village(request):
        if request.method == 'POST':
                form = AnimatorAssignedVillageForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/animatorassignedvillages/')
                else:
                        return render_to_response('add_animator_assigned_village.html',{'form':form})
        else:
                form = AnimatorAssignedVillageForm()
                return render_to_response('add_animator_assigned_village.html',{'form':form})


def animator_assigned_village(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('animator_assigned_village')
        else:
                animator_assigned_villages = AnimatorAssignedVillage.objects.order_by("-id")
                return render_to_response('animator_assigned_village.html', {'animator_assigned_villages': animator_assigned_villages})

def add_animator(request):
	AnimatorAssignedVillageInlineFormSet = inlineformset_factory(Animator, AnimatorAssignedVillage, extra=3)
        if request.method == 'POST':
                form = AnimatorForm(request.POST)
		formset = AnimatorAssignedVillageInlineFormSet(request.POST, request.FILES)
	
                if form.is_valid() and formset.is_valid():
                        saved_animator = form.save()
			#formset.save_m2m()
			animator = Animator.objects.get(pk=saved_animator.id)
			formset = AnimatorAssignedVillageInlineFormSet(request.POST, request.FILES, instance=animator)
			formset.save()
                        return HttpResponseRedirect('/dashboard/animators/')
                else:
                        return render_to_response('add_animator.html',{'form':form, 'formset':formset})
        else:
                form = AnimatorForm()
		formset = AnimatorAssignedVillageInlineFormSet()
                return render_to_response('add_animator.html',{'form':form, 'formset':formset})


def animator(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('animator')
        else:
                animators = Animator.objects.order_by("-id")
                return render_to_response('animators.html', {'animators': animators})



def add_field_officer(request):
        if request.method == 'POST':
                form = FieldOfficerForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/fieldofficers/')
                else:
                        return render_to_response('add_fo.html',{'form':form})
        else:
                form = FieldOfficerForm()
                return render_to_response('add_fo.html',{'form':form})


def field_officer(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('field_officer')
        else:
                fieldofficers = FieldOfficer.objects.order_by("-id")
                return render_to_response('fos.html', {'fieldofficers': fieldofficers})


def add_partner(request):
        if request.method == 'POST':
                form = PartnerForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/partners/')
                else:
                        return render_to_response('add_partner.html',{'form':form})
        else:
                form = PartnerForm()
                return render_to_response('add_partner.html',{'form':form})


def partner(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('partner')
        else:
                partners = Partners.objects.order_by("-id")
                return render_to_response('partners.html', {'partners': partners})


def add_person(request):
        if request.method == 'POST':
                form = PersonForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/persons/')
                else:
                        return render_to_response('add_person.html',{'form':form})
        else:
                form = PersonForm()
                return render_to_response('add_person.html',{'form':form})


def person(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('person')
        else:
                persons = Person.objects.order_by("-id")
                return render_to_response('persons.html', {'persons': persons})


def add_practice(request):
        if request.method == 'POST':
                form = PracticeForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/practices/')
                else:
                        return render_to_response('add_practice.html',{'form':form})
        else:
                form = PracticeForm()
                return render_to_response('add_practice.html',{'form':form})


def practice(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('practice')
        else:
                practices = Practices.objects.order_by("-id")
                return render_to_response('practices.html', {'practices': practices})



def add_village(request):
        PersonGroupInlineFormSet = inlineformset_factory(Village, PersonGroups, extra=5)
	AnimatorInlineFormSet = inlineformset_factory(Village, Animator, extra=5)
        if request.method == 'POST':
                form = VillageForm(request.POST)
                formset_person_group = PersonGroupInlineFormSet(request.POST, request.FILES)
		formset_animator = AnimatorInlineFormSet(request.POST, request.FILES)

                if form.is_valid() and formset_person_group.is_valid() and formset_animator.is_valid():
                        saved_village = form.save()
                        #formset.save_m2m()
                        village = Village.objects.get(pk=saved_village.id)
                        formset_person_group = PersonGroupInlineFormSet(request.POST, request.FILES, instance=village)
			formset_animator = AnimatorInlineFormSet(request.POST, request.FILES, instance = village)
                        formset_person_group.save()
			formset_animator.save()
                        return HttpResponseRedirect('/dashboard/villages/')
                else:
                        return render_to_response('add_village.html',{'form':form, 'formset_person_group':formset_person_group, 'formset_animator':formset_animator})
        else:
                form = VillageForm()
                formset_person_group = PersonGroupInlineFormSet()
		formset_animator = AnimatorInlineFormSet()
                return render_to_response('add_village.html',{'form':form,'formset_person_group':formset_person_group,'formset_animator':formset_animator })


def village(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('village')
        else:
                villages = Village.objects.order_by("-id")
                return render_to_response('villages.html', {'villages': villages})


def add_video(request):
        if request.method == 'POST':
                form = VideoForm(request.POST)
                if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/dashboard/videos/')
                else:
                        return render_to_response('add_video.html',{'form':form})
        else:
                form = VideoForm()
                return render_to_response('add_video.html',{'form':form})


def video(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('video')
        else:
                videos = Video.objects.order_by("-id")
                return render_to_response('videos.html', {'videos': videos})


def add_screening(request):
        PersonMeetingAttendanceInlineFormSet = inlineformset_factory(Screening, PersonMeetingAttendance, extra=2)
        if request.method == 'POST':
                form = ScreeningForm(request.POST)
                formset = PersonMeetingAttendanceInlineFormSet(request.POST, request.FILES)

                if form.is_valid() and formset.is_valid():
                        saved_screening = form.save()
                        #formset.save_m2m()
                        screening = Screening.objects.get(pk=saved_screening.id)
                        formset = PersonMeetingAttendanceInlineFormSet(request.POST, request.FILES, instance=screening)
                        formset.save()
                        return HttpResponseRedirect('/dashboard/screenings/')
                else:
                        return render_to_response('add_screening.html',{'form':form, 'formset':formset})
        else:
                form = ScreeningForm()
                formset = PersonMeetingAttendanceInlineFormSet()
                #json_subcat1 = serializers.serialize("json", form)
		#json_subcat2 = serializers.serialize("json", formset)
                #return HttpResponse(json_subcat , mimetype="application/javascript")
		#return HttpResponse("{'form': %s, 'formset': %s}" % (json_subcat1, json_subcat2))
                return render_to_response('add_screening.html',{'form':form, 'formset':formset})


def screening(request):
        if request.method == 'POST':
                # This should handle the region DELETE request

                # Now redirect back to ourselves as a GET to re-render the page
                return redirect('screening')
        else:
                screenings = Screening.objects.order_by("-id")
                return render_to_response('screenings.html', {'screenings': screenings})
               
def test_view(request):
	    #Book.objects.filter(title__icontains=q)
	   
        q = Village.objects.raw('select * from dg_village')
        return render_to_response('results.html',{'body': "%s" % q})
    
	   



