
import json
import requests
import models

from types import StringType, MethodType
from django.conf.urls import include, patterns, url
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.views.generic import View
from models import Call

from views import AudioView, CallEndView, PassthruView, MissedCallView

# Exotel's uptime information available for everyone to see at http://status.exotel.in.

class ExotelService(object):
    time_limit="500"  # This is optional
    time_out="500" # This is also optional
    call_type="trans" # "trans" for transactional and "promo" for promotional content
    flow_urlformat = 'http://my.exotel.in/exoml/start/{flow_id}/'
    initiate_call_urlformat = 'https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'
    views = {}
    # {url1: (url_type, func1), url2: (url_type, func1), url3: (url_type, func1)}
    
    def __init__(self):
        class_name = "CallEndView{0}".format(self.name)
        self.ServiceCallEndView = type(class_name, (CallEndView,), {})
    
    def __init__(self, service_name, sid, token, caller_id, flow_id):
        self.name = service_name
        self.sid = sid
        self.token = token
        self.caller_id = caller_id
        self.flow_id = flow_id
        self.__init__()
    
    def init_state(self):
        return {}
    
    def init_props(self):
        return {}
    
    def init_call(self, mobile_number):
        call_url = self.initiate_call_urlformat.format(sid=self.sid)
        flow_url = self.flow_urlformat.format(flow_id=self.flow_id)
        #TODO create a call object. add the id to the CustomField. save the call object
        props = self.init_props()
        post_data = {
            'From' :  int(mobile_number),
            'CallerId' : self.caller_id,
            'Url' : flow_url,
            'TimeLimit' : self.time_limit,
            'TimeOut' : self.time_out,
            'CallType' : self.call_type,
            'StatusCallback' : reverse(self.ServiceCallEndView.get_name()),
            'CustomField' : json.dumps(props),
        }
        r = requests.post(call_url, auth=(self.sid, self.token), data=post_data)
        response_data = json.loads(r.text)
        call_sid = response_data['Call']['Sid']
        call = Call(exotel_call_id = call_sid)
        call.state = json.dumps(self.init_state())
        call.props = json.dumps(self.init_props())
        call.save()
        #return {"id": call.id, "exotel_id": call_sid}
        return {"exotel_id": call_sid}
    
    def urlpatterns(self):
        endurl = url(r'^end/$', self.ServiceCallEndView.as_view(), name=self.ServiceCallEndView.get_name())
        urls = [endurl]
        
        for url_endpoint, (url_type, view_func) in self.views.iteritems():
            class_name = "View{0}_{1}".format(self.name, url_endpoint)
            if url_type == 'audio':
                if type(view_func) is StringType:
                    MyView = type(class_name, (AudioView,), {'audio_url': view_func})
                elif type(view_func) is MethodType:
                    MyView = type(class_name, (AudioView,), {'process': view_func})
                else:
                    raise Exception("View function type incorrect")
            elif url_type == 'passthru':
                MyView = type(class_name, (PassthruView,), {'process': view_func})
            elif url_type == 'missedcall':
                MyView = type(class_name, (MissedCallView,), {'process': view_func})
            else:
                raise Exception("View type should be audio or passthru")
            urls.append(url(r'^{0}/'.format(url_endpoint), MyView.as_view()))
        
        urlpatterns = patterns('', url(r'^{0}/'.format(self.name), include(urls)))
        return urlpatterns
