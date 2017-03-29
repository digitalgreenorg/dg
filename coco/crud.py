from videos.models import Video
from videos.models import NonNegotiable
from people.models import Animator
from people.models import AnimatorAssignedVillage
from people.models import PersonGroup
from people.models import Person
from activities.models import Screening
from activities.models import PersonAdoptPractice


def crud_of_video(data_dict, production_team, create, update):
    if create and not update:
        video, created = Video.objects.get_or_create(**data_dict)
    elif update and not create:
        video = Video.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        video.update(**data_dict)
        video = video.latest('id')
    if len(production_team):
        video.production_team.add(*production_team)
    return


def save_data_in_animator(data_dict, assigned_villages):
    animator_obj, created = Animator.objects.get_or_create(**data_dict)
    for item in assigned_villages:
        obj = AnimatorAssignedVillage.objects.get_or_create(village_id=item, animator_id=animator_obj.id)

    return 

def crud_of_group(data_dict, create, update):
    if create and not update:
        persongroup_obj, created = PersonGroup.objects.get_or_create(**data_dict)
    elif update and not create:
        persongroup_obj = PersonGroup.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        persongroup_obj.update(**data_dict)
        persongroup_obj = mediator_obj.latest('id')
    return
    

def crud_of_nonnegotiable(data_dict, create, update):
    if create and not update:
        nonnegotiable, created = NonNegotiable.objects.get_or_create(**data_dict)
    elif update and not create:
        nonnegotiable = NonNegotiable.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        nonnegotiable.update(**data_dict)
        nonnegotiable = nonnegotiable.latest('id')
    return


def crud_of_person(data_dict, create, update):
    if create and not update:
        person, created = Person.objects.get_or_create(**data_dict)
    elif update and not create:
        person = Person.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        person.update(**data_dict)
        person = person.latest('id')
    return
    


def save_data_in_adoption(data_dict, videoes_screened, farmer_groups_targeted, farmers_attendance):
    pap_obj, created = PersonAdoptPractice.objects.get_or_create(**data_dict)
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


def crud_of_adoption(data_dict, create, update, user_id, partner_id):
    if create and not update:
        pap_obj, created = PersonAdoptPractice.objects.get_or_create(**data_dict)
    elif update and not create:
        pap_obj = PersonAdoptPractice.objects.filter(id=data_dict.get('_id'))
        del data_dict['_id']
        pap_obj.update(**data_dict)
        pap_obj = pap_obj.latest('id')
    return


def crud_of_screening(data_dict, videoes_screened, farmer_groups_targeted,
                      farmers_attendance, create, update):
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
    # through table
    if farmers_attendance:
        for item in farmers_attendance:
            PersonMeetingAttendance.objects.get_or_create(person_id=item,
                                                          screening_id=scr_obj.id,
                                                          user_created_id=_data_dict.get('user_created_id'),
                                                          user_modified_id=_data_dict.get('user_modified_id'))
    return
