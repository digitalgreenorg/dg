import inspect
import json
import time

from types import StringType, TupleType
from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.views.generic import View

from exception_email import sendmail

from models import Call

class ExotelView(View):
    @classmethod
    def exotel_response(cls, request, payload, status=200):
        callSid = request.GET["CallSid"]
        props = request.GET["CustomField"]
        frm = request.GET["From"]
        to = request.GET["To"]
        response = HttpResponse(payload, content_type="text/plain", status=status)
        response["CallSid"] = callSid
        response["From"] = frm
        response["To"] = to
        response["DialWhomNumber"] = ""
        response["CustomField"] =  props
        return response

class CallEndView(ExotelView):
    @classmethod
    def get_name(cls):
        return cls.__name__
    
    @classmethod
    def get(cls, request):
        #TODO retrieve the call object and save the status of the call
        #TODO end_call should be called from a URL which is sent above as statuscallback
        response = HttpResponse(status = 200)
        try: 
            call_id = request.GET["CallSid"]
            call = Call.objects.get(exotel_call_id=call_id)
            #final_response_dict = json.loads(request)
            call.end(response = request.GET)
            response = cls.exotel_response(request, 0)
        except Exception as e:
            error = "Error: " + e + request
            sendmail("Error in ending call", error)
        return response

class AudioView(ExotelView):
    @classmethod
    def get(cls, request):
        audio_url = None
        call_id = request.GET["CallSid"]
        props = request.GET["CustomField"]
        if hasattr(cls, 'audio_url'):
            audio_url = cls.audio_url
        else:
            args = (inspect.getargspec(cls.process)).args
            # The view needs to use both state, which is dynamic, and properties, that are fixed for a call
            if 'props' in args and 'state' in args:
                try:
                    call = Call.objects.get(exotel_call_id=call_id)
                    state = json.loads(call.state)
                    ret_val = cls.process(props, state)
                    # The view returns only the URL of the audio file
                    if type(ret_val) == StringType:
                        audio_url = ret_val
                    # The view returns the URL of the audio file AND needs to change the state in the database
                    elif type(ret_val) == TupleType:
                        audio_url = ret_val[0]
                        new_state = ret_val[1]
                        call.state = json.dumps(new_state)
                        call.save()
                except Exception as e:
                    error = "Error in IVR" + str(error)
                    sendmail("Error in saving call", error)
                else:
                    raise Exception("Process function defined incorrectly.")
            # The view uses properties fixed at the beginning of the call to identify the audio url
            elif 'props' in args:
                audio_url = cls.process(props)
            else:
                raise Exception("Process function defined incorrectly.")
        
        response = cls.exotel_response(request, audio_url)
        return response

class PassthruView(ExotelView):    
    @classmethod
    def get(cls, request):
        call_id = request.GET["CallSid"]
        props = request.GET["CustomField"]
        call = Call.objects.get(exotel_call_id=call_id)
        state = json.loads(call.state)
        (status, new_state) = cls.process(props, state)
        call.state = json.dumps(new_state)
        call.save()
        response = cls.exotel_response(request, None, status=status)
        return response

class MissedCallView(ExotelView):
    @classmethod
    def get(cls, request):
        call_id = request.GET["CallSid"]
        props = request.GET["From"]
        # TODO create a call in the db. save it's details.
        time.sleep(5) # sleep for 5 seconds to hope that the initial missed call has been finished by then. MAYBE NOT NEEDED
        status = cls.process(props)
        return HttpResponse(status=200) #We don't need to send a response because passthru is asynchronous 
