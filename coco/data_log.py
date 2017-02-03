import json

from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import get_model
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.db import IntegrityError, transaction

class TimestampException(Exception):
    pass

class UserDoesNotExist(Exception):
    pass


def upload_entries(sender, **kwargs):
    from coco.models import CocoUser
    instance = kwargs["instance"]
    if kwargs["created"]:
        a = instance.upload_file.read()
        d = json.loads(a)
        user_object = User.objects.get(username=d['user']['username'])
        instance.user = user_object
        instance.save()
        partner = CocoUser.objects.get(user=user_object).partner
        upload_entries = d['uploads']
        for entry in upload_entries:
            if str(entry['action']) == 'A':
                globals()[str(entry['entity_name']) + '_add'](entry['data'], user_object.id, partner.id, d)
            if str(entry['action']) == 'E':
                globals()[str(entry['entity_name']) + '_edit'](entry['data'], user_object.id, partner.id, d, entry['id'])


def mediator_add(data, user_id, partner_id, d):
    from people.models import Animator, AnimatorAssignedVillage
    try:
        obj = Animator(user_created_id=user_id, user_modified_id=user_id, name=data['name'],
                       gender=data['gender'],
                       phone_no=data['phone_no'] if data['phone_no'] != None else "",
                       partner_id=partner_id,
                       district_id=data['district']['id'])
        with transaction.atomic():
            obj.save()
        for vil in data["assigned_villages"]:
            obj_vil = AnimatorAssignedVillage(animator_id=obj.id, village_id=vil['id'])
            obj_vil.save()
    except IntegrityError:
        print "Duplicate Mediator Entry"


def mediator_edit(data, user_id, partner_id, d, entry_id):
    from people.models import Animator, AnimatorAssignedVillage
    if 'online_id' in data:
        mediator_obj = Animator.objects.get(id=data['online_id'])
    else:
        try:
            mediator_obj = Animator.objects.get(name=data['name'],
                                                gender=data['gender'],
                                                district_id=data['district']['id'],
                                                partner_id=partner_id)
        except Animator.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'mediator' and entry['data']['id'] == data['id']:

                    mediator_obj = Animator.objects.get(name=entry['data']['name'],
                                                        gender=entry['data']['gender'],
                                                        district_id=entry['data']['district']['id'],
                                                        partner_id=partner_id)
                    break
    mediator_obj.user_modified_id = user_id
    mediator_obj.name = data['name']
    mediator_obj.gender = str(data['gender'])
    mediator_obj.phone_no = data['phone_no'] if data['phone_no'] != None else ""
    mediator_obj.partner_id = partner_id
    mediator_obj.district_id = data['district']['id']
    mediator_obj.save()
    AnimatorAssignedVillage.objects.filter(animator_id=mediator_obj.id).delete()
    for vil in data["assigned_villages"]:
        obj_vil = AnimatorAssignedVillage(animator_id=mediator_obj.id, village_id=vil['id'])
        obj_vil.save()


def group_add(data, user_id, partner_id, d):
    from people.models import PersonGroup
    try:
        obj = PersonGroup(user_created_id=user_id, user_modified_id=user_id,
                          group_name=data['group_name'],
                          partner_id=partner_id,
                          village_id=data['village']['id'])
        with transaction.atomic():
            obj.save()
    except IntegrityError:
        print "Group Already Exists"


def group_edit(data, user_id, partner_id, d, entry_id):
    from people.models import PersonGroup
    if 'online_id' in data:
        group_obj = PersonGroup.objects.get(id=data['online_id'])
    else:
        try:
            group_obj = PersonGroup.objects.get(group_name=data['group_name'], village_id=data['village']['id'])
        except PersonGroup.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'group' and entry['data']['id'] == data['id']:

                    group_obj = PersonGroup.objects.get(group_name=entry['data']['group_name'], village_id=entry['data']['village']['id'])
                    break
    group_obj.user_modified_id = user_id
    group_obj.group_name = data['group_name']
    group_obj.partner_id = partner_id
    group_obj.village_id = data['village']['id']
    group_obj.save()


def person_add(data, user_id, partner_id, d):
    from people.models import Person, PersonGroup
    group_id = None
    if data['group']['id'] is not None:
        for entry in d['group']:
            if entry['id'] == data['group']['id']:
                if 'online_id' in entry:
                    group_id = entry['online_id']
                else:
                    group_object = PersonGroup.objects.get(group_name=entry['group_name'], village_id=entry['village']['id'])
                    group_id = group_object.id
                break
    try:
        obj = Person(user_created_id=user_id, user_modified_id=user_id, 
                     person_name=data['person_name'],
                     father_name=data['father_name'],
                     village_id=data['village']['id'],
                     gender=data['gender'],
                     age=data['age'],
                     phone_no=data['phone_no'] if data['phone_no'] != None else "",
                     group_id=group_id,
                     partner_id=partner_id)
        with transaction.atomic():
            obj.save()
    except IntegrityError:
        print "Person Already Exists"


def person_edit(data, user_id, partner_id, d, entry_id):
    from people.models import Person, PersonGroup
    if 'online_id' in data:
        person_obj = Person.objects.get(id=data['online_id'])
    else:
        try:
            person_obj = Person.objects.get(person_name=data['person_name'],
                                            father_name=data['father_name'],
                                            village_id=data['village']['id'])
        except Person.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'person' and entry['data']['id'] == data['id']:

                    group_obj = PersonGroup.objects.get(group_name=entry['data']['group_name'], village_id=entry['data']['village']['id'])
                    break
    group_id = None
    if data['group']['id'] is not None:
        for entry in d['group']:
            if entry['id'] == data['group']['id']:
                if 'online_id' in entry:
                    group_id = entry['online_id']
                else:
                    group_object = PersonGroup.objects.get(group_name=entry['group_name'], village_id=entry['village']['id'])
                    group_id = group_object.id
                break
    person_obj.user_modified_id = user_id
    person_obj.person_name = data['person_name']
    person_obj.father_name = data['father_name']
    person_obj.village_id = data['village']['id']
    person_obj.gender = data['gender']
    person_obj.age = data['age']
    person_obj.phone_no = data['phone_no'] if data['phone_no'] != None else ""
    person_obj.group_id = group_id
    person_obj.partner_id = partner_id
    person_obj.save()


def video_add(data, user_id, partner_id, d):
    from people.models import Animator, Person, PersonGroup
    from videos.models import Video

    facilitator_id = None
    cameraoperator_id = None
    for entry in d['mediator']:
        if entry['id'] == data['facilitator']['id']:
            if 'online_id' in entry:
                facilitator_id = entry['online_id']
            else:
                facilitator_object = Animator.objects.get(name=entry['name'],
                                                          gender=entry['gender'],
                                                          district_id=entry['district']['id'],
                                                          partner_id=entry['partner']['id'])
                facilitator_id = facilitator_object.id
        if entry['id'] == data['cameraoperator']['id']:
            if 'online_id' in entry:
                cameraoperator_id = entry['online_id']
            else:
                cameraoperator_object = Animator.objects.get(name=entry['name'],
                                                             gender=entry['gender'],
                                                             district_id=entry['district']['id'],
                                                             partner_id=entry['partner']['id'])
                cameraoperator_id = cameraoperator_object.id
    try:
        obj = Video(user_created_id=user_id, user_modified_id=user_id,
                    title=data['title'], 
                    video_type=data['video_type'],
                    language_id=data['language']['id'],
                    summary=data['summary'] if data['summary'] != None else "",
                    video_production_start_date=data['video_production_start_date'],
                    video_production_end_date=data['video_production_end_date'],
                    village_id=data['village']['id'],
                    facilitator_id=facilitator_id,
                    cameraoperator_id=cameraoperator_id,
                    video_suitable_for=data['video_suitable_for'],
                    actors=data['actors'],
                    approval_date=data['approval_date'],
                    youtubeid=data['youtubeid'] if data['youtubeid'] != None else "",
                    partner_id=partner_id)
        with transaction.atomic():
            obj.save()
        for person in data['farmers_shown']:
            for entry in d['person']:
                if entry['id'] == person['id']:
                    if 'online_id' in entry:
                        person_obj = Person.objects.get(id=entry['online_id'])
                    else:
                        person_obj = Person.objects.get(person_name=entry['person_name'],
                                                        father_name=entry['father_name'],
                                                        village_id=entry['village']['id'])
                        obj.farmers_shown.add(person_obj)
        obj.save()
    except:
        print "Video Already Exists"


def video_edit(data, user_id, partner_id, d, entry_id):
    from people.models import Animator, Person
    from videos.models import Video
    if 'online_id' in data:
        video_obj = Video.objects.get(id=data['online_id'])
    else:
        try:
            video_obj = Video.objects.get(title=data['title'],
                                          video_production_start_date=data['video_production_start_date'],
                                          video_production_end_date=data['video_production_end_date'],
                                          village_id=data['village']['id'])
        except Video.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'video' and entry['data']['id'] == data['id']:

                    video_obj = Video.objects.get(title=entry['data']['title'],
                                                  video_production_start_date=entry['data']['video_production_start_date'],
                                                  video_production_end_date=entry['data']['video_production_end_date'],
                                                  village_id=entry['data']['village']['id'])
                    break
    facilitator_id = None
    cameraoperator_id = None
    for entry in d['mediator']:
        if entry['id'] == data['facilitator']['id']:
            if 'online_id' in entry:
                facilitator_id = entry['online_id']
            else:
                facilitator_object = Animator.objects.get(name=entry['name'],
                                                          gender=entry['gender'],
                                                          district_id=entry['district']['id'],
                                                          partner_id=entry['partner']['id'])
                facilitator_id = facilitator_object.id
        if entry['id'] == data['cameraoperator']['id']:
            if 'online_id' in entry:
                cameraoperator_id = entry['online_id']
            else:
                cameraoperator_object = Animator.objects.get(name=entry['name'],
                                                             gender=entry['gender'],
                                                             district_id=entry['district']['id'],
                                                             partner_id=entry['partner']['id'])
                cameraoperator_id = cameraoperator_object.id
    video_obj.user_modified_id = user_id
    video_obj.title = data['title']
    video_obj.video_type = data['video_type']
    video_obj.language_id = data['language']['id']
    video_obj.summary = data['summary'] if data['summary'] != None else ""
    video_obj.video_production_start_date = data['video_production_start_date']
    video_obj.video_production_end_date = data['video_production_end_date']
    video_obj.village_id = data['village']['id']
    video_obj.facilitator_id = facilitator_id
    video_obj.cameraoperator_id = cameraoperator_id
    video_obj.video_suitable_for = data['video_suitable_for']
    video_obj.actors = data['actors']
    video_obj.approval_date = data['approval_date']
    video_obj.youtubeid = data['youtubeid'] if data['youtubeid'] != None else ""
    video_obj.partner_id = partner_id
    video_obj.save()
    video_obj.farmers_shown.all().delete()

    for person in data['farmers_shown']:
        for entry in d['person']:
            if entry['id'] == person['id']:
                if 'online_id' in entry:
                    person_obj = Person.objects.get(id=entry['online_id'])
                else:
                    person_obj = Person.objects.get(person_name=entry['person_name'],
                                                    father_name=entry['father_name'],
                                                    village_id=entry['village']['id'])
                video_obj.farmers_shown.add(person_obj)
    video_obj.save()
    # Take care of non-negotiables


def nonnegotiable_add(data, user_id, partner_id, d):
    from videos.models import NonNegotiable, Video
    video_id = None
    for entry in d['video']:
        if entry['id'] == data['video']['id']:
            if 'online_id' in entry:
                video_id = entry['online_id']
            else:
                video_object = Video.objects.get(title=entry['title'],
                                                 video_production_start_date=entry['video_production_start_date'],
                                                 video_production_end_date=entry['video_production_end_date'],
                                                 village_id=entry['village']['id'])
                video_id = video_object.id

    obj = NonNegotiable(user_created_id=user_id, user_modified_id=user_id,
                        non_negotiable=data['non_negotiable'],
                        physically_verifiable=True if data['physically_verifiable'] != None else False,
                        video_id=video_id)
    obj.save()


def adoption_add(data, user_id, partner_id, d):
    from activities.models import PersonAdoptPractice
    from people.models import Person
    from videos.models import Video
    video_id = None
    for entry in d['video']:
        if entry['id'] == data['video']['id']:
            if 'online_id' in entry:
                video_id = entry['online_id']
            else:
                video_object = Video.objects.get(title=entry['title'],
                                                 video_production_start_date=entry['video_production_start_date'],
                                                 video_production_end_date=entry['video_production_end_date'],
                                                 village_id=entry['village']['id'])
                video_id = video_object.id

    person_id = None
    for entry in d['person']:
        if entry['id'] == data['person']['id']:
            if 'online_id' in entry:
                person_id = entry['online_id']
            else:
                person_object = Person.objects.get(person_name=entry['person_name'],
                                                   father_name=entry['father_name'],
                                                   village_id=entry['village']['id'])
                person_id = person_object.id
    try:
        obj = PersonAdoptPractice(user_created_id=user_id, user_modified_id=user_id,
                                  video_id=video_id,
                                  person_id=person_id,
                                  partner_id=partner_id,
                                  date_of_adoption=data['date_of_adoption']
                                  )
        with transaction.atomic():
            obj.save()
    except IntegrityError:
        print "Adoption Already Exists"


def adoption_edit(data, user_id, partner_id, d, entry_id):
    from activities.models import PersonAdoptPractice
    from people.models import Person
    from videos.models import Video
    if data['online_id']:
        pap_obj = PersonAdoptPractice.objects.get(id=data['online_id'])
    else:
        try:
            pap_obj = PersonAdoptPractice.objects.get(person_id=data['person']['id'],
                                                      video_id=data['video']['id'],
                                                      date_of_adoption=data['date_of_adoption'])
        except PersonAdoptPractice.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'adoption' and entry['data']['id'] == data['id']:

                    pap_obj = PersonAdoptPractice.objects.get(person_id=entry['data']['person']['id'],
                                                              video_id=entry['data']['video']['id'],
                                                              date_of_adoption=entry['data']['date_of_adoption'])
                    break
    video_id = None
    for entry in d['video']:
        if entry['id'] == data['video']['id']:
            if 'online_id' in entry:
                video_id = entry['online_id']
            else:
                video_object = Video.objects.get(title=entry['title'],
                                                 video_production_start_date=entry['video_production_start_date'],
                                                 video_production_end_date=entry['video_production_end_date'],
                                                 village_id=entry['village']['id'])
                video_id = video_object.id

    person_id = None
    for entry in d['person']:
        if entry['id'] == data['person']['id']:
            if 'online_id' in entry:
                person_id = entry['online_id']
            else:
                person_object = Person.objects.get(person_name=entry['person_name'],
                                                   father_name=entry['father_name'],
                                                   village_id=entry['village']['id'])
                person_id = person_object.id

    pap_obj.user_modified_id = user_id
    pap_obj.video_id = video_id
    pap_obj.person_id = person_id
    pap_obj.partner_id = partner_id
    pap_obj.date_of_adoption = data['date_of_adoption']
    pap_obj.save()


def screening_add(data, user_id, partner_id, d):
    from activities.models import Screening
    from people.models import Animator, Person, PersonGroup
    from videos.models import Video

    animator_id = None
    for entry in d['mediator']:
        if entry['id'] == data['animator']['id']:
            if 'online_id' in entry:
                animator_id = entry['online_id']
            else:
                animator_object = Animator.objects.get(name=entry['name'],
                                                          gender=entry['gender'],
                                                          district_id=entry['district']['id'],
                                                          partner_id=entry['partner']['id'])
                animator_id = animator_object.id
    try:
        obj = Screening(user_created_id=user_id, user_modified_id=user_id,
                        date=data['date'],
                        start_time=data['start_time'],
                        end_time=data['end_time'],
                        village_id=data['village']['id'],
                        animator_id=animator_id,
                        partner_id=partner_id
                        )
        with transaction.atomic():
            obj.save()

        for group in data['farmer_groups_targeted']:
            for entry in d['group']:
                if entry['id'] == group['id']:
                    if 'online_id' in entry:
                        group_obj = PersonGroup.objects.get(id=entry['online_id'])
                    else:
                        group_obj = PersonGroup.objects.get(group_name=entry['group_name'], village_id=entry['village']['id'])
                    obj.farmer_groups_targeted.add(group_obj)
                    break
        obj.save()
        for video in data['videoes_screened']:
            for entry in d['video']:
                if entry['id'] == video['id']:
                    if 'online_id' in entry:
                        video_obj = Video.objects.get(id=entry['online_id'])
                    else:
                        video_obj = Video.objects.get(title=entry['title'],
                                                      video_production_start_date=entry['video_production_start_date'],
                                                      video_production_end_date=entry['video_production_end_date'],
                                                      village_id=entry['village']['id'])
                    obj.videoes_screened.add(video_obj)
                    break
        obj.save()
        save_pma(data["farmers_attendance"], user_id, obj.id, d)
    except IntegrityError:
        print "Screening Already Exists"


def screening_edit(data, user_id, partner_id, d, entry_id):
    from activities.models import PersonMeetingAttendance, Screening
    from people.models import Animator, PersonGroup
    from videos.models import Video
    if data['online_id']:
        screening_obj = Screening.objects.get(id=data['online_id'])
    else:
        try:
            screening_obj = Screening.objects.get(date=data['date'],
                                                  start_time=data['start_time'],
                                                  end_time=data['end_time'],
                                                  animator_id=data['animator']['id'],
                                                  village_id=data['village']['id'])
        except Screening.DoesNotExist:
            for entry in d['uploads'][int(entry_id)-2::-1]:
                if entry['entity_name'] == 'screening' and entry['data']['id'] == data['id']:
                    screening_obj = Screening.objects.get(date=entry['data']['date'],
                                                          start_time=entry['data']['start_time'],
                                                          end_time=entry['data']['end_time'],
                                                          animator_id=entry['data']['animator']['id'],
                                                          village_id=entry['data']['village']['id'])
                    break
    animator_id = None
    for entry in d['mediator']:
        if entry['id'] == data['animator']['id']:
            if 'online_id' in entry:
                animator_id = entry['online_id']
            else:
                animator_object = Animator.objects.get(name=entry['name'],
                                                       gender=entry['gender'],
                                                       district_id=entry['district']['id'],
                                                       partner_id=entry['partner']['id'])
                animator_id = animator_object.id

    screening_obj.user_modified_id = user_id
    screening_obj.date = data['date']
    screening_obj.start_time = data['start_time']
    screening_obj.end_time = data['end_time']
    screening_obj.village_id = data['village']['id']
    screening_obj.animator_id = animator_id
    screening_obj.partner_id = partner_id
    screening_obj.save()
    screening_obj.farmer_groups_targeted.all().delete()
    for group in data['farmer_groups_targeted']:
        for entry in d['group']:
            if entry['id'] == group['id']:
                if 'online_id' in entry:
                    group_obj = PersonGroup.objects.get(id=entry['online_id'])
                else:
                    group_obj = PersonGroup.objects.get(group_name=entry['group_name'], village_id=entry['village']['id'])
                screening_obj.farmer_groups_targeted.add(group_obj)
                break
    screening_obj.save()
    screening_obj.videoes_screened.all().delete()
    for video in data['videoes_screened']:
        for entry in d['video']:
            if entry['id'] == video['id']:
                if 'online_id' in entry:
                    video_obj = Video.objects.get(id=entry['online_id'])
                else:
                    video_obj = Video.objects.get(title=entry['title'],
                                                  video_production_start_date=entry['video_production_start_date'],
                                                  video_production_end_date=entry['video_production_end_date'],
                                                  village_id=entry['village']['id'])
                    screening_obj.videoes_screened.add(video_obj)
                    break
    screening_obj.save()
    PersonMeetingAttendance.objects.filter(screening_id=screening_obj.id).delete()
    save_pma(data["farmers_attendance"], user_id, screening_obj.id, d)


def save_pma(pmas, user_id, screening_id, d):
    from activities.models import PersonMeetingAttendance
    from people.models import Person
    from videos.models import Video
    for pma in pmas:
        video_id = None
        if pma["expressed_adoption_video"]["id"] != None:
            for entry in d['video']:
                if entry['id'] == pma["expressed_adoption_video"]['id']:
                    if 'online_id' in entry:
                        video_id = entry['online_id']
                    else:
                        video_obj = Video.objects.get(title=entry['title'],
                                                     video_production_start_date=entry['video_production_start_date'],
                                                     video_production_end_date=entry['video_production_end_date'],
                                                     village_id=entry['village']['id'])
                        video_id = video_obj.id
                        break
        for entry in d['person']:
            if str(entry['id']) == str(pma['person_id']):
                print "came here"
                if 'online_id' in entry:
                    person_id = entry['online_id']
                else:
                    person_obj = Person.objects.get(person_name=entry['person_name'],
                                                    father_name=entry['father_name'],
                                                    village_id=entry['village']['id'])
                    person_id = person_obj.id
                    break
        obj = PersonMeetingAttendance(user_created_id=user_id, user_modified_id=user_id,
                                      screening_id=screening_id,
                                      person_id=person_id,
                                      interested=True if pma['interested'] == 'true' else False,
                                      expressed_question=pma['expressed_question'],
                                      expressed_adoption_video_id=video_id)
        obj.save()


def save_log(sender, **kwargs ):
    instance = kwargs["instance"]
    action = kwargs["created"]
    sender = sender.__name__    # get the name of the table which sent the request
    model_dict = model_to_dict(instance)
    previous_time_stamp = get_latest_timestamp()
    try:
        user = User.objects.get(id = instance.user_modified_id) if instance.user_modified_id else User.objects.get(id = instance.user_created_id)
    except Exception, ex:
        user = None
    
    # Adding PersonMeetingAttendance records to the ServerLog. This is required for Mobile COCO, since we need to update a person record, whenever a pma is edited or deleted. We are adding the instance.person.id since the corresponding person record needs to be updated whenever an attendance record is changed.
    model_id = instance.person.id if sender is "PersonMeetingAttendance" else instance.id
    print model_id
    if sender == "Village":
        village_id = instance.id
    elif sender == "Animator" or sender == 'Language' or sender == 'NonNegotiable' or sender == 'Category' or sender == 'SubCategory'or sender == 'VideoPractice':
        village_id = None
    elif sender == "PersonAdoptPractice":
        village_id = instance.person.village.id
    else:
        village_id = instance.village.id
    partner_id = None if sender in ["Village", 'Language', 'NonNegotiable', 'Category', 'SubCategory', 'VideoPractice'] else instance.partner.id

    ServerLog = get_model('coco', 'ServerLog')
    log = ServerLog(village=village_id, user=user, action=action, entry_table=sender,
                    model_id=model_id, partner=partner_id)
    log.save()
    ###Raise an exception if timestamp of latest entry is less than the previously saved data timestamp
    if previous_time_stamp:
        if previous_time_stamp.timestamp > log.timestamp:
            raise TimestampException('timestamp error: Latest entry data time created is less than previous data timecreated')


def delete_log(sender, **kwargs):
    instance = kwargs["instance"]
    sender = sender.__name__    # get the name of the table which sent the request
    user = None
    if instance.user_created_id:
        if instance.user_modified_id:
            user = User.objects.get(id=instance.user_modified_id) 
        else:
            user = User.objects.get(id=instance.user_created_id)
    # Adding PersonMeetingAttendance records to the ServerLog. This is required for Mobile COCO, since we need to update a person record, whenever a pma is edited or deleted. We are adding the instance.person.id since the corresponding person record needs to be updated whenever an attendance record is changed.
    model_id = instance.person.id if sender is "PersonMeetingAttendance" else instance.id
    ServerLog = get_model('coco', 'ServerLog')
    try:
        log = ServerLog(village=instance.village.id, user=user, action=-1, entry_table=sender, model_id=instance.id, partner=instance.partner.id)
        log.save()
    except Exception as ex:
        pass


def send_updated_log(request):
    timestamp = request.GET.get('timestamp', None)
    if timestamp:
        CocoUser = get_model('coco', 'CocoUser')
        CocoUserVillages = get_model('coco', 'CocoUser_villages')
        try:
            coco_user = CocoUser.objects.get(user_id=request.user.id)
        except Exception as e:
            raise UserDoesNotExist('User with id: ' + str(request.user.id) + 'does not exist')
        partner_id = coco_user.partner_id
        villages = CocoUserVillages.objects.filter(cocouser_id=coco_user.id).values_list('village_id', flat=True)
        ServerLog = get_model('coco', 'ServerLog')
        rows = ServerLog.objects.filter(timestamp__gte=timestamp, entry_table__in=['Animator', 'Video', 'NonNegotiable'])
        if partner_id:
            rows = rows | ServerLog.objects.filter(timestamp__gte=timestamp, village__in=villages, partner=partner_id )
        else:
            rows = rows | ServerLog.objects.filter(timestamp__gte=timestamp, village__in=villages)
        if rows:
            data = serializers.serialize('json', rows, fields=('action','entry_table','model_id', 'timestamp'))
            return HttpResponse(data, content_type="application/json")
    return HttpResponse("0")


def get_latest_timestamp():
    ServerLog = get_model('coco', 'ServerLog')
    try:
        timestamp = ServerLog.objects.latest('id')
    except Exception as e:
        timestamp = None
    return timestamp
