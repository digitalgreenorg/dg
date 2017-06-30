import json
from django.db.models import get_model
from videos.models import Video
from videos.models import NonNegotiable
from people.models import Animator
from people.models import AnimatorAssignedVillage
from people.models import PersonGroup
from people.models import Person
from activities.models import Screening
from activities.models import PersonAdoptPractice
from activities.models import PersonMeetingAttendance
from videos.models import DirectBeneficiaries


def crud_of_model(model, app, data_dict, create, update): 
    model = get_model(app, model)
    if create and not update:
        obj, created = model.objects.get_or_create(**data_dict)
    elif update and not create:
        obj = model.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        obj.update(**data_dict)
        obj = obj.latest('id')
    return


def crud_of_video(data_dict, production_team, videopractice, create, update):
    if create and not update:
        video, created = Video.objects.get_or_create(**data_dict)
    elif update and not create:
        video = Video.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        video.update(**data_dict)
        video = video.latest('id')
    if len(production_team):
        video.production_team.add(*production_team)
    if len(videopractice):
        video.videopractice.add(*videopractice)
    return



def crud_of_mediator(data_dict, assigned_villages, create, update):
    if create and not update:
        mediator_obj, created = Animator.objects.get_or_create(**data_dict)
    elif update and not create:
        mediator_obj = Animator.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        mediator_obj.update(**data_dict)
        mediator_obj = mediator_obj.latest('id')
    if len(assigned_villages):
        for item in assigned_villages:
            obj = \
                AnimatorAssignedVillage.objects.get_or_create(village_id=item,
                                                              animator_id=mediator_obj.id,
                                                              user_created_id=data_dict.get('user_created_id'),
                                                              user_modified_id=data_dict.get('user_modified_id')
                                                              )
    return


def crud_of_screening(data_dict, videoes_screened, farmer_groups_targeted,
                      farmers_attendance, frontlineworkerpresent, create, update):
    if create and not update:
        scr_obj, created = Screening.objects.get_or_create(**data_dict)
    elif update and not create:
        scr_obj = Screening.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        scr_obj.update(**data_dict)
        scr_obj = scr_obj.latest('id')
    if videoes_screened:
        scr_obj.videoes_screened.add(*videoes_screened)
        scr_obj.save()
    if farmer_groups_targeted:
        scr_obj.farmer_groups_targeted.add(*farmer_groups_targeted)
        scr_obj.save()
    if frontlineworkerpresent:
        scr_obj.frontlineworkerpresent.add(*frontlineworkerpresent)
        scr_obj.save()
    # through table
    if farmers_attendance:
        for item in farmers_attendance:
            pma_obj, created = \
                PersonMeetingAttendance.objects.get_or_create(person_id=item.get('id'),
                                                              screening_id=scr_obj.id,
                                                              user_created_id=data_dict.get('user_created_id'),
                                                              user_modified_id=data_dict.get('user_modified_id')
                                                              )
            # saving direct beneficiaries
            if item.get('category') is not None:
                for iterable in item.get('category'):
                    obj = DirectBeneficiaries.objects.get(id=int(iterable.get('id')))
                    pma_obj.category = json.dumps([obj.id])
                    pma_obj.save()
            # updating the person age & gender
            try:
                person_obj = Person.objects.get(id=item.get('id'))
                person_obj.age = item.get('age')
                person_obj.gender = item.get('gender')
                person_obj.save()

            except:
                pass

    return
