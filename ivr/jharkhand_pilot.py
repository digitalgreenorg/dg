from exotel import ExotelService
from views import CallEndView
from models import Broadcast, IvrSubscriber
import time
import json

from dg.settings import EXOTEL_TOKEN

class JharkhandPilot(ExotelService):
    name = "jharkhand_pilot"
    #TODO some of these must come from settings
    sid = "digitalgreen2"
    token = EXOTEL_TOKEN
    caller_id="01139595020"
    flow_id = "51319"
    views = {}
    
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]

        self.views = {
            # 'greeting': ('audio', "http://audiofile"  + self.name),
            # 'message': ('audio', self.get_required_message),
            # 'ivr_menu': ('audio', "http://ivr_menu_audio_file"),
            # 'ivr_menu_repeat': ('passthru', self.revert_state),
            'nth_hello': ('audio', self.get_nth_hello),
            'missed_call': ('missedcall', self.init_call),
        }
        class_name = "CallEndView{0}".format(self.name)
        self.ServiceCallEndView = type(class_name, (CallEndView,), {'name':class_name})
        #super(HelloBye, self).__init__()
    
    def init_state(self):
        state = {
            "n": 1
        }
        return state
    
    def init_props(self):
        # we need a to init the district of person
        props = {}
        return props

    def get_nth_hello(self, props, state, from_no):
        n = state["n"]
        #audio = "http://hello{0}".format(n) + self.name
        channels = IvrSubscriber.objects.get(phone_no = from_no).channels.all()
        broadcasts = Broadcast.objects.filter(channels__contains = channels).order_by('id') # not sure about this filter SHOULD BE DESCENDING ORDER
        audio = broadcasts[n].audio.audiofile
        audio = "https://s3.amazonaws.com/dg_ivrs/bihar_pilot/hindi_audios/moong_adoption_question.mp3"
        state["n"] = n+1
        return (audio, state)

    def get_required_message(self, props, state):
        #get call object and check state, change the state, return the required audio.
        n = state["n"]
        state["n"] = n+1
        return ("http://audiofile", state)

    def revert_state(self, props, state):
        n=state["n"]
        state["n"] = n-1

