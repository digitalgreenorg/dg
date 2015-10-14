from exotel import ExotelService
from views import CallEndView
import time

class JharkhandPilot(ExotelService):
    name = "jharkhand_pilot"
    #TODO some of these must come from settings
    sid = "digitalgreen2"
    token = "421c11b1235067ca30ca87590c80c31eadc46af0"
    caller_id="01139595020"
    flow_id = "51319"
    views = {}
    
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.views = {
            'greeting': ('audio', "http://audiofile"  + self.name),
            'message': ('audio', self.get_required_message),
            'ivr_menu': ('audio', "http://ivr_menu_audio_file"),
            'ivr_menu_repeat': ('passthru', self.revert_state),
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
        props = {}
        return props

    def get_required_message(self, props, state):
        #get call object and check state, change the state, return the required audio.
        n = state["n"]
        state["n"] = n+1
        return ("http://audiofile", state)

    def revert_state(self, props, state):
        n=state["n"]
        state["n"] = n-1

