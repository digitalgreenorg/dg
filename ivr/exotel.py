
import json
import requests
import models

from django.conf.urls import include, patterns, url
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.views.generic import View

from applets import GreetingApplet

# Exotel's uptime information available for everyone to see at http://status.exotel.in.

class CallEndView(View):
    @classmethod
    def get_name(cls):
        return '{0}_end'.format(cls.name)
    
    @classmethod  
    def get(cls, request):
        #TODO retrieve the call object and save the status of the call
        #TODO end_call should be called from a URL which is sent above as statuscallback
        return HttpResponse(0)

class ExotelService(object):
    time_limit="500"  # This is optional
    time_out="500" # This is also optional
    call_type="trans" # "trans" for transactional and "promo" for promotional content
    flow_urlformat = 'http://my.exotel.in/exoml/start/{flow_id}/'
    initiate_call_urlformat = 'https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'
    custom_field = ''
    #TODO  make a standard status callback that records the usual stuff
    
    def __init__(self, service_name, sid, token, caller_id, flow_id, **kwargs):
        self.name = service_name
        self.sid = sid
        self.token = token
        self.caller_id = caller_id
        self.flow_id = flow_id
        self.applets = []
        for key, value in kwargs.items():
            setattr(self, key, value)
        end_view_class = '{0}CallEndView'.format(self.name)
        end_view_name = '{0}_end'.format(self.name)
        self.EndViewClass = type(end_view_class, (CallEndView,), {'name':end_view_name})
    
    def init_call(self, mobile_number, info=None):
        call_url = initiate_call_urlformat.format(sid=self.sid)
        flow_url = flow_urlformat.format(flow_id=self.flow_id)
        
        #TODO create a call object. add the id to the CustomField. save the call object
        post_data = {
            'From' :  int(mobile_number),
            'CallerId' : self.caller_id,
            'Url' : flow_url,
            'TimeLimit' : self.time_limit,
            'TimeOut' : self.time_out,
            'CallType' : self.call_type,
            'StatusCallback' : reverse(self.EndViewClass.name())
        }
        
        if info:
            post_data['CustomField'] =  json.dumps(info.__dict__)
        
        r = requests.post(call_url, auth=(self.sid, self.token), data=post_data)
        response_data = json.loads(r.text)
        call_id = response_data['Call']['Sid']
        #TODO update the call object based on the response
        call = models.Call(response_data['Call'])
        return call_id
    
    def add_applet(self, applet):
        self.applets.append(applet)
    
    def urlpatterns(self, read_urls=False):        
        endurl = url(r'^end/$'.format(self.name), self.EndViewClass.as_view(), name=self.EndViewClass.get_name())
        pattern_list = [endurl]
        for applet in self.applets:
            pattern_list.extend(applet.urlpatterns(self.name))
        urlpatterns = patterns('', url(r'^{0}/'.format(self.name), include(pattern_list, 'ivrs', self.name)))
        return urlpatterns
    
    class Meta:
        abstract=True


