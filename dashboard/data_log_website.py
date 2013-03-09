from website.models import *
from dashboard import models
from django.http import HttpResponse

ACTION = dict({
    'delete':-1,
    'edit'  : 0,
    'add'   : 1
})

def update_website(request):
    # timestamp = request.GET['timestamp']
    rows = models.ServerLog.objects.filter(id = 11)
    for row in rows:
        print "Processing additions for " + row.entry_table
        if row.entry_table == 'Person':
            update_person(row)
    return HttpResponse("1")

def update_person(object):
    if object.action == ACTION['delete']:
        farmer = Farmer.objects.filter(uid = object.model_id)
        farmer.delete()
    elif object.action == ACTION['add']:    
        person = models.Person.objects.get(id = object.model_id)
        farmer = Farmer(uid=person.id, name=person.person_name, thumbnailURL="", imageURL="", village=person.village.village_name, block = person.village.block.block_name, 
                       district = person.village.block.district.district_name, state = person.village.block.district.state.state_name, 
                       country = person.village.block.district.state.country.country_name)
        farmer.save()
        partner_id = object.partner # getting partner from serverlog table
        partner = Partner.objects.get(uid = partner_id)
        partner.farmers.add(farmer)
    elif object.action == ACTION['edit']:
        person = models.Person.objects.get(id = object.model_id)
        farmer = Farmer.objects.get(uid  = object.model_id)
        farmer.update(name=person.person_name, village=person.village.village_name, block = person.village.block.block_name, 
                       district = person.village.block.district.district_name, state = person.village.block.district.state.state_name, 
                       country = person.village.block.district.state.country.country_name,thumbnailURL="", imageURL="")
        farmer.save()
        
    
    