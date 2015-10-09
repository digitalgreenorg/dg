from exotel import ExotelService
from views import CallEndView

import json

class HelloBye(ExotelService):
    name = "hello_bye"
    #TODO some of these must come from settings
    sid = "digitalgreen2"
    token = "421c11b1235067ca30ca87590c80c31eadc46af0"
    caller_id="01139595020"
    flow_id = "54820"
    views = {}
    
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.views = {
            'hello': ('audio', "https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi_introduction.mp3"),
            'daily_hello': ('audio', "https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi_introduction.mp3"),
            'nth_hello': ('audio', "https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/hindi_introduction.mp3"),
            'all_the_way': ('passthru', self.all_the_way),
            'missed_call': ('missedcall', self.init_call),
        }
        class_name = "CallEndView{0}".format(self.name)
        self.ServiceCallEndView = type(class_name, (CallEndView,), {'name':class_name})
        #super(HelloBye, self).__init__()
    
    def init_state(self):
        state = {
            "n": 0
        }
        return state
    
    def init_props(self):
        props = {
            "day": "Monday"
        }
        return props
    
    def all_the_way(self, props, state):
        if state["n"] is 3:
            state["all the way"] = True
            status = 200
        else:
            state["all the way"] = False
            status = 305
        return (status, state)
    
    def get_nth_hello(self, props, state):
        n = state["n"]
        audio = "http://hello{0}".format(n) + self.name
        state["n"] = n+1
        return (audio, state)
    
    def get_daily_greeting(self, props):
        properties = json.loads(props)
        day_of_week = properties["day"]
        return "http://hello{0}".format(day_of_week) + self.name
        
