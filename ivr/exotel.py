from django.db import models
import json
import requests

from django.conf.urls import include, patterns, url
from applets import GreetingApplet

# Exotel's uptime information available for everyone to see at http://status.exotel.in.

class ExotelService(object):
    time_limit="500"  # This is optional
    time_out="500" # This is also optional
    call_type="trans" # "trans" for transactional and "promo" for promotional content
    flow_urlformat = 'http://my.exotel.in/exoml/start/{flow_id}/'
    initiate_call_urlformat = 'https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'
    custom_field = ''
    status_callback = ''
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
        }
        try:
            post_data['StatusCallback'] = self.call_end_url
        except AttributeError:
            pass
        if info:
            post_data['CustomField'] =  json.dumps(info.__dict__)
        
        r = requests.post(call_url, auth=(self.sid, self.token), data=post_data)
        response_data = json.loads(r.text)
        call_id = response_data['Call']['Sid']
        #TODO update the call object based on the response
        return call_id
    
    def end_call(self, request):
        #TODO retrieve the call object and save the status of the call
        #TODO end_call should be called from a URL which is sent above as statuscallback
        print "something"
    
    def add_applet(self, applet):
        self.applets.append(applet)
        
    def urlpatterns(self):
        pattern_list = []
        for applet in self.applets:
            pattern_list.extend(applet.urlpatterns(self.name))
        urlpatterns = patterns('', url(r'^{0}/'.format(self.name), include(pattern_list)))
        return urlpatterns
    
    class Meta:
        abstract=True


