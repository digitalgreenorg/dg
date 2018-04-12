import sys

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from hello_bye import HelloBye
from jharkhand_pilot import JharkhandPilot
from urls import hello, greeting, jharkhand_pilot
from models import Call, Broadcast

from people.models import Animator

class CallAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['exotel_call_id', 'attributes', 'state',]
                          }
                  )]
    list_display = ('exotel_call_id', 'attributes', 'state',)
    search_fields =['exotel_call_id',]

class ChannelAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['name',]
                          }
                  )]
    list_display = ('name',)
    search_fields =['name',]

class IvrSubscriberAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['name', 'phone_no',]
                          }
                  )]
    list_display = ('name', 'phone_no',)
    search_fields =['name', 'phone_no',]


class AudioAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['audio_file', 'title', 'description', 'audio_status',]
                          }
                  )]
    list_display = ('audio_file', 'title', 'description', 'audio_status',)
    search_fields =['title',]

class BroadcastAdmin(admin.ModelAdmin):
    fieldsets = [(None,  {'fields': ['service', 'audio_file', 'channels', 'schedule_call',]
                          }
                  )]
    list_display = ('service', 'audio_file', 'district_list', 'schedule_call',)
    search_fields =['service','district',]

    def district_list(self, obj):
        return "\n".join([p.district_name for p in obj.district.all()])

    def save_model(self, request, obj, form, change):
      obj.save()
      ivr_service = obj.service

      #ivr_obj = eval(ivr_service)()
      if ivr_service == 'hello':
        ivr_obj = hello
        #update audio URL accordingly
      elif ivr_service == 'greeting':
        ivr_obj = greeting
      elif ivr_service == 'jharkhand_pilot':
        ivr_obj = jharkhand_pilot
      else:
        print "Too Bad!"

        animator_list = Animator.objects.filter(district__in=obj.district.all())
        for person in animator_list:
          if person.phone_no:
            pass
            #print type(person.phone_no)
            #ivr_obj.init_call(person.phone_no)
