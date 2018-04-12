# from crud import *
#
#
# def format_data_or_saving_in_adoption(request, data_dict, user_id, partner_id):
#     person = data_dict.get('person')
#     video = data_dict.get('video')
#     animator = data_dict.get('animator')
#     date_of_adoption = data_dict.get('date_of_adoption')
#     date_of_verification = data_dict.get('date_of_verification')
#     partner = partner_id
#     online_id = data_dict.get('online_id')
#     verification_status = data_dict.get('verification_status')
#     non_negotiable_check = data_dict.get('non_negotiable_check')
#     verified_by = data_dict.get('observation_status')
#     parentcategory = data_dict.get('parentcategory')
#     adopt_practice = data_dict.get('adopt_practice')
#     adopt_practice_second = data_dict.get('adopt_practice_second')
#     krp_one = data_dict.get('krp_one')
#     krp_two = data_dict.get('krp_two')
#     krp_three = data_dict.get('krp_three')
#     krp_four = data_dict.get('krp_four')
#     krp_five = data_dict.get('krp_five')
#     user_created_id = user_id
#     _data_dict = {'user_created_id': user_created_id, 'partner_id': partner_id,
#                  'person_id': person.get('id') if person else person,
#                  'video_id': video.get('id') if video else video,
#                  'animator_id': animator.get('id') if animator else animator,
#                  'date_of_adoption': date_of_adoption,
#                  'date_of_verification': date_of_verification,
#                  'partner_id': partner,
#                  'parentcategory_id': parentcategory.get('id') if parentcategory else parentcategory,
#                  'verification_status': verification_status if verification_status else 0,
#                  'non_negotiable_check': non_negotiable_check,
#                  'adopt_practice': adopt_practice,
#                  'adopt_practice_second': adopt_practice_second,
#                  'krp_one': krp_one,
#                  'krp_two': krp_two,
#                  'krp_three': krp_three,
#                  'krp_four': krp_four,
#                  'krp_five': krp_five,
#                  'verified_by': verified_by}
#
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_model("PersonAdoptPractice", "activities", _data_dict, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_model("PersonAdoptPractice", "activities", _data_dict, create, update)
#     return
#
#
# def checkm2mvalidation(data_list):
#     if len(filter(None, data_list)):
#         return data_list
#     else:
#         return False
#
#
# def format_data_or_saving_in_screening(request, data_dict, user_id, partner_id):
#     create = False
#     update = False
#     date = data_dict.get('date')
#     start_time = data_dict.get('start_time')
#     end_time = data_dict.get('end_time')
#     location = data_dict.get('location')
#     village = data_dict.get('village')
#     animator = data_dict.get('animator')
#     online_id = data_dict.get('online_id')
#     parentcategory = data_dict.get('parentcategory')
#     questions_asked = data_dict.get('questions_asked')
#     partner = partner_id
#     verification_status = data_dict.get('verification_status')
#     observation_status = data_dict.get('observation_status')
#     screening_grade = data_dict.get('screening_grade')
#     observer = data_dict.get('observer')
#     videoes_screened = [iterable.get('id') for iterable in data_dict.get('videoes_screened')]
#     farmer_groups_targeted = [iterable.get('id') for iterable in data_dict.get('farmer_groups_targeted')]
#     farmers_attendance = [{'id': int(iterable.get('person_id')), 'age': iterable.get('age'), 'gender': iterable.get('gender'), 'category': iterable.get('category')} for iterable in data_dict.get('farmers_attendance')]
#     frontlineworkerpresent = [iterable.get('id') for iterable in data_dict.get('frontlineworkerpresent')]
#     health_provider_present = data_dict.get('health_provider_present')
#     type_of_video = data_dict.get('type_of_video')
#     type_of_venue = data_dict.get('type_of_venue')
#     meeting_topics = data_dict.get('meeting_topics')
#
#
#     _data_dict = {'user_created_id': user_id, 'partner_id': partner_id,
#                   'user_modified_id': user_id,
#                  'start_time': start_time,
#                  'date': date,
#                  'end_time': end_time,
#                  'animator_id': animator.get('id') if animator else animator,
#                  'village_id': village.get('id') if village else village,
#                  'partner_id': partner,
#                  'questions_asked': questions_asked,
#                  'screening_grade': screening_grade,
#                  'observer': observer,
#                  'parentcategory_id': parentcategory.get('id') if parentcategory else parentcategory,
#                  'observation_status': observation_status if observation_status else 0,
#                  'health_provider_present': health_provider_present,
#                  'type_of_video': type_of_video,
#                  'type_of_venue': type_of_venue,
#                  'meeting_topics': meeting_topics,
#                  }
#     videoes_screened = videoes_screened if checkm2mvalidation(videoes_screened) else False
#     farmer_groups_targeted = checkm2mvalidation(farmer_groups_targeted)
#     farmers_attendance = checkm2mvalidation(farmers_attendance)
#     frontlineworkerpresent = checkm2mvalidation(frontlineworkerpresent)
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_screening(_data_dict, videoes_screened,
#                           farmer_groups_targeted,
#                           farmers_attendance,
#                           frontlineworkerpresent,
#                           create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_screening(_data_dict, videoes_screened,
#                           farmer_groups_targeted,
#                           farmers_attendance,
#                           frontlineworkerpresent,
#                           create, update)
#
#     return
#
# def format_data_or_saving_in_person(request, data_dict, user_id, partner_id):
#     person_name = data_dict.get('person_name')
#     father_name = data_dict.get('father_name')
#     age = data_dict.get('age')
#     gender = data_dict.get('gender')
#     phone_no = data_dict.get('phone_no')
#     village = data_dict.get('village')
#     group = data_dict.get('group')
#     date_of_joining = data_dict.get('date_of_joining')
#     image_exists = False
#     partner = data_dict.get('partner')
#     is_modelfarmer = data_dict.get('is_modelfarmer') if data_dict.get('is_modelfarmer') else False
#     user_created_id = user_id
#     online_id = data_dict.get('online_id')
#     partner_id = partner_id
#     _data_dict = {'partner_id': partner_id,
#                  'user_created_id': user_created_id,
#                  'user_modified_id': user_id,
#                  'is_modelfarmer': is_modelfarmer,
#                  'group_id': group.get('id') if group else None,
#                  'age': age,
#                  'gender': gender,
#                  'person_name': person_name,
#                  'father_name': father_name,
#                  'phone_no': phone_no,
#                  'partner_id': partner_id,
#                  'village_id': village.get('id') if village else None,
#                  'date_of_joining': date_of_joining,
#                  'image_exists': image_exists,
#                  'is_modelfarmer': is_modelfarmer
#                  }
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_model("Person", "people", _data_dict, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_model("Person", "people", _data_dict, create, update)
#     return
#
# def format_data_or_saving_in_group(request, data_dict, user_id, partner_id):
#     group_name = data_dict.get('group_name')
#     village = data_dict.get('village')
#     partner = data_dict.get('partner')
#     online_id = data_dict.get('online_id')
#     _data_dict = {'group_name': group_name,
#                  'village_id': village.get('id') if village else village,
#                  'partner_id': partner_id,
#                  'user_created_id': user_id,
#                  'user_modified_id': user_id}
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_model('PersonGroup', 'people', _data_dict, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_model('PersonGroup', 'people', _data_dict, create, update)
#     return
#
# def format_data_or_saving_in_mediator(request, data_dict, user_id, partner_id):
#     name = data_dict.get('name')
#     gender = data_dict.get('gender')
#     phone_no = data_dict.get('phone_no')
#     partner = data_dict.get('partner')
#     district = data_dict.get('district')
#     online_id = data_dict.get('online_id')
#     assigned_villages = [iterable.get('id') for iterable in data_dict.get('assigned_villages')]
#     total_adoptions = data_dict.get('total_adoptions')
#     role = data_dict.get('role')
#     _data_dict = {'name': name, 'gender': gender, 'phone_no': phone_no,
#                  'partner_id': partner_id, 'user_created_id': user_id,
#                  'user_modified_id': user_id, 'total_adoptions': total_adoptions if total_adoptions else 0,
#                  'district_id': district.get('id') if district else district}
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_mediator(_data_dict, assigned_villages, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_mediator(_data_dict, assigned_villages, create, update)
#     # crud_of_mediator(data_dict, assigned_villages)
#     return
#
#
# def format_data_or_saving_in_nonnegotiable(request, data_dict, user_id, partner_id):
#     video = data_dict.get('video')
#     non_negotiable = data_dict.get('non_negotiable')
#     physically_verifiable = data_dict.get('physically_verifiable')
#     user_created_id = user_id
#     user_modified_id = user_id
#     online_id = data_dict.get('online_id')
#     partner_id = partner_id
#     _data_dict = {'video_id': video.get('id') if video else video,
#                  'non_negotiable': non_negotiable,
#                  'physically_verifiable': physically_verifiable,
#                  'user_created_id': user_created_id,
#                  'user_modified_id': user_modified_id,
#                  }
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_model("NonNegotiable", "videos", _data_dict, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_model("NonNegotiable", "videos", _data_dict, create, update)
#
#
# def format_data_or_saving_in_video(request, data_dict, user_id, partner_id):
#     # formatting for video
#     related_practice = data_dict.get('related_practice')
#     partner = data_dict.get('partner')
#     language = data_dict.get('language')
#     category = data_dict.get('category')
#     subcategory = data_dict.get('subcategory')
#     videopractice = [int(iterable.get('id')) for iterable in data_dict.get('videopractice')]
#     title = data_dict.get('title')
#     video_type = data_dict.get('video_type')
#     benefit = data_dict.get('benefit')
#     village = data_dict.get('village')
#     youtubeid = data_dict.get('youtubeid')
#     online_id = data_dict.get('online_id')
#     review_status = data_dict.get('review_status')
#     reviewer = data_dict.get('reviewer')
#     reviewed_by = data_dict.get('reviewed_by')
#     online_id = data_dict.get('online_id')
#     approval_date = data_dict.get('approval_date')
#     video_grade = data_dict.get('video_grade')
#     production_team = [int(iterable.get('id')) for iterable in data_dict.get('production_team')]
#     production_date = data_dict.get('production_date')
#     duration = data_dict.get('duration')
#     _data_dict = {'category_id': category.get('id') if category else category,
#                  'subcategory_id': subcategory.get('id') if subcategory else subcategory,
#                  'title': title,
#                  'language_id': language.get('id') if language else language,
#                  'video_type': video_type,
#                  'benefit': benefit,
#                  'approval_date': approval_date,
#                  'duration': duration,
#                  'production_date': production_date,
#                  'review_status': review_status if review_status else 0,
#                  'reviewer': reviewer,
#                  'reviewed_by': reviewed_by,
#                  'video_grade': video_grade,
#                  'youtubeid': youtubeid,
#                  'village_id': village.get('id') if village else village,
#                  'user_created_id': user_id,
#                  'user_modified_id': user_id,
#                  'partner_id': partner_id
#                  }
#     _data_dict = dict((k, v) for k, v in _data_dict.iteritems() if v)
#     # for new entries
#     if data_dict.get('online_id') is not None:
#         create = False
#         update = True
#         _data_dict['_id'] = online_id
#         crud_of_video(_data_dict, production_team, create, update)
#     # for updating existing entries
#     if not data_dict.get('online_id') and data_dict.get('id'):
#         create = True
#         update = False
#         crud_of_video(_data_dict, production_team, videopractice, create, update)
#
#     return