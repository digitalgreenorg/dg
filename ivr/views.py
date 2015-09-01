import inspect
import json

from types import StringType, TupleType
from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.views.generic import View

from models import Call

class CallEndView(View):
    @classmethod
    def get_name(cls):
        return cls.__name__
    
    @classmethod
    def get(cls, request):
        #TODO retrieve the call object and save the status of the call
        #TODO end_call should be called from a URL which is sent above as statuscallback
        call_id = request.GET["CallSid"]
        call = Call.objects.get(exotel_call_id=call_id)
        final_response_dict = json.loads(request)
        call.end(final_response_dict = final_response_dict)
        return HttpResponse(0)

class AudioView(View):
    @classmethod
    def get(cls, request):
        audio_url = None
        
        call_id = request.GET["CallSid"]
        props = json.loads(request.GET["CustomField"])
        if hasattr(cls, 'audio_url'):
            audio_url = cls.audio_url
        else:
            args = (inspect.getargspec(cls.process)).args
            if 'props' in args and 'state' in args:
                call = Call.objects.get(exotel_call_id=call_id)
                state = json.loads(call.state)
                ret_val = cls.process(props, state)
                if type(ret_val) == StringType:
                    audio_url = ret_val
                elif type(ret_val) == TupleType:
                    audio_url = ret_val[0]
                    new_state = ret_val[1]
                    call.state = json.dumps(new_state)
                    call.save()
                else:
                    raise Exception("Process function defined incorrectly.")
            elif 'props' in args:
                audio_url = cls.process(props)
            else:
                raise Exception("Process function defined incorrectly.")
        
        return HttpResponse(audio_url, status=200)

class PassthruView(View):
      
    @classmethod
    def get(cls, request):
        call_id = request.GET["CallSid"]
        props = request.GET["CustomField"]
        call = Call.objects.get(exotel_call_id=call_id)
        state = json.loads(call.state)
        (status, new_state) = self.process(audio_url_format, props, state)
        call.state = json.dumps(new_state)
        call.save()
        return HttpResponse(status=status)




    
