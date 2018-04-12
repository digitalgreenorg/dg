# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import HttpResponse, Http404, HttpResponseBadRequest
# from django.shortcuts import redirect, render_to_response, HttpResponseRedirect
# from django.template import RequestContext
# # from models import CocoUser
# # from programs.models import Partner
# # from geographies.models import State
# # from geographies.models import District
# # from geographies.models import Village
# # from videos.models import Video
# # from base_models import TYPE_OF_COCOUSER
# import json

# def is_change_from(full_path):
#     coco_user_id = full_path.split('/')[-2:]
#     coco_user_id = coco_user_id[0] if coco_user_id[0].isdigit() else coco_user_id[1] if coco_user_id[1].isdigit() else ''
#     return coco_user_id
#
# @login_required
# def add_cocouser(request):
#     context = RequestContext(request)
#     change_form_flag = 0
#     template_variables = dict()
#     if request.method == 'GET':
#         auth_user_list = User.objects.values('id','username')
#         partner_list = Partner.objects.values('id','partner_name')
#         state_list = State.objects.values('id','state_name')
#         type_of_cocouser_list = [{'value':value,'showing_text':showing_text} for value,showing_text in TYPE_OF_COCOUSER]
#         coco_user_id = is_change_from(request.get_full_path())
#         template_variables['title'] = "Add coco user"
#         if coco_user_id != '':
#             change_form_flag = 1
#             try:
#                 coco_user_obj = CocoUser.objects.get(id=coco_user_id)
#             except Exception as e:
#                 message = "coco user object with primary key u'%s' does not exist."%(coco_user_id)
#                 raise Http404(message)
#             current_user_videos = coco_user_obj.videos.values('id', 'title')
#             current_villages = coco_user_obj.villages.values('id','village_name','block__block_name','block__district__district_name','block__district__state__state_name')
#             current_user_villages = []
#             for village in current_villages:
#                 current_user_villages.append({'id':village['id'],'village_name':'%s [%s] [%s] [%s]'%(village['village_name'],village['block__block_name'],village['block__district__district_name'],village['block__district__state__state_name'])})
#             current_auth_user_id = coco_user_obj.user_id
#             current_partner_id = coco_user_obj.partner_id
#             current_type_of_cocouser = coco_user_obj.type_of_cocouser
#             template_variables['current_auth_user_id'] = current_auth_user_id
#             template_variables['current_partner_id'] = current_partner_id
#             template_variables['current_type_of_cocouser'] = current_type_of_cocouser
#             template_variables['current_user_videos'] = current_user_videos
#             template_variables['current_user_villages'] = current_user_villages
#             template_variables['title'] = "Change coco user"
#         template_variables['auth_user_list'] = auth_user_list
#         template_variables['partner_list'] = partner_list
#         template_variables['type_of_cocouser_list'] = type_of_cocouser_list
#         template_variables['state_list'] = state_list
#         template_variables['change_form_flag'] = change_form_flag
#         return render_to_response('admin/coco/cocouser/change_form.html',template_variables,context)
#     elif request.method == 'POST':
#         if not all(objects in request.POST for objects in ['user', 'partner', 'village']):
#             return HttpResponseBadRequest("User, partner and village is required")
#         coco_user_id = is_change_from(request.get_full_path())
#         user = request.POST.getlist('user')[0]
#         if CocoUser.objects.filter(user_id=user).exists() and coco_user_id == '':
#             message = "coco user with \"%s\" User already exists. Select different User."%(CocoUser.objects.get(user_id=user).user.username)
#             messages.add_message(request, messages.ERROR, message)
#             return HttpResponseRedirect(".")
#         partner = request.POST.getlist('partner')[0]
#         type_of_cocouser = request.POST.getlist('type_of_cocouser')[0]
#         villages = request.POST.getlist('village')
#         if 'video' in request.POST:
#             videos = request.POST.getlist('video')
#         else:
#             videos = []
#         if coco_user_id != '':
#             change_form_flag = 1
#             try:
#                 coco_user_obj = CocoUser.objects.get(id=coco_user_id)
#             except Exception as e:
#                 message = "coco user object with primary key u'%s' does not exist."%(coco_user_id)
#                 raise Http404(message)
#             if int(user) != coco_user_obj.user_id:
#                 if CocoUser.objects.filter(user_id=user).exists():
#                     message = "coco user with \"%s\" User already exists. Select different User."%(CocoUser.objects.get(user_id=user).user.username)
#                     messages.add_message(request, messages.ERROR, message)
#                     return HttpResponseRedirect(".")
#                 coco_user_obj.user_id = user
#                 coco_user_obj.save()
#             if partner != coco_user_obj.partner_id:
#                 coco_user_obj.partner_id = partner
#                 coco_user_obj.save()
#             if type_of_cocouser != coco_user_obj.type_of_cocouser:
#                 coco_user_obj.type_of_cocouser = type_of_cocouser
#                 coco_user_obj.save()
#             new_village_set = set(map(int,villages))
#             new_video_set = set(map(int,videos))
#             old_village_set = set(coco_user_obj.villages.values_list('id',flat=True))
#             old_video_set = set(coco_user_obj.videos.values_list('id',flat=True))
#             coco_user_obj.villages.remove(*list(old_village_set-new_village_set))
#             coco_user_obj.villages.add(*list(new_village_set-old_village_set))
#             coco_user_obj.videos.remove(*list(old_video_set-new_video_set))
#             coco_user_obj.videos.add(*list(new_video_set-old_video_set))
#             if '_save' in request.POST:
#                 message = "The coco user \"%s\" was changed successfully."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/'
#             elif '_addanother' in request.POST:
#                 message = "The coco user \"%s\" was changed successfully. You may add another qa coco user below."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/add/'
#             elif '_continue' in request.POST:
#                 message = "The coco user \"%s\" was changed successfully. You may edit it again below."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/%s/'%(coco_user_id)
#             else:
#                 return HttpResponseBadRequest("BAD REQUEST")
#             messages.add_message(request, messages.SUCCESS, message)
#             return redirect(redirect_to)
#         else:
#             if CocoUser.objects.filter(user_id=user).exists():
#                 message = "coco user with \"%s\" User already exists. Select different User."%(CocoUser.objects.get(user_id=user).user.username)
#                 messages.add_message(request, messages.ERROR, message)
#                 return HttpResponseRedirect(".")
#             coco_user_obj = CocoUser(user_id=user,partner_id=partner,type_of_cocouser=type_of_cocouser)
#             try:
#                 coco_user_obj.save()
#             except Exception as e:
#                 message = "Something is wrong. Contact system team with below error.\n%s"%(str(e))
#                 messages.add_message(request, messages.ERROR, message)
#                 return HttpResponseRedirect(".")
#             for village in villages:
#                 coco_user_obj.villages.add(village)
#             for video in videos:
#                 coco_user_obj.videos.add(video)
#
#             if '_save' in request.POST:
#                 message = "The coco user \"%s\" was added successfully."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/'
#             elif '_addanother' in request.POST:
#                 message = "The coco user \"%s\" was added successfully. You may add another qa coco user below."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/add/'
#             elif '_continue' in request.POST:
#                 message = "The coco user \"%s\" was added successfully. You may edit it again below."%(coco_user_obj.user.username)
#                 redirect_to = '/coco/admin/coco/cocouser/%s/'%(coco_user_obj.id)
#             else:
#                 return HttpResponseBadRequest("BAD REQUEST")
#             messages.add_message(request, messages.SUCCESS, message)
#             return redirect(redirect_to)
#     else:
#         return HttpResponseBadRequest("<h2>Only GET and POST requests is allow</h2>")
#
# @login_required
# def state_wise_district(request):
#     state_id = request.GET.getlist('state_id')[0]
#     district_list = list(District.objects.filter(state_id=state_id).values('id','district_name'))
#     district_list = json.dumps(district_list)
#     return HttpResponse(district_list)
#
# @login_required
# def district_wise_village(request):
#     district_id = request.GET.getlist('district_id')[0]
#     all_villages = Village.objects.filter(block__district_id=district_id).values('id','village_name','block__block_name','block__district__district_name','block__district__state__state_name')
#     village_list = []
#     for village in all_villages:
#         village_list.append({'id':village['id'],'village_name':'%s [%s] [%s] [%s]'%(village['village_name'],village['block__block_name'],village['block__district__district_name'],village['block__district__state__state_name'])})
#     village_list = json.dumps(village_list)
#     return HttpResponse(village_list)
#
# @login_required
# def partner_wise_video(request):
#     partner_id = request.GET.getlist('partner_id')[0]
#     video_list = list(Video.objects.filter(partner_id=partner_id).values('id','title'))
#     video_list = json.dumps(video_list)
#     return HttpResponse(video_list)
