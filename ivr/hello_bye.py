from exotel import ExotelService
from applets import GreetingApplet

class HelloBye(ExotelService):
    name = "hello_bye"
    #TODO some of these must come from settings
    sid = "digitalgreen2"
    token = "421c11b1235067ca30ca87590c80c31eadc46af0"
    caller_id="01130018178"
    flow_id = "27037"
    
    def __init__(self, name, **kwargs):
        try:
            hello_audio = kwargs["hello_audio"]
        except AttributeError:
            hello_audio = "http://helloaudiofile"+name
        try:
            bye_audio = kwargs["bye_audio"]
        except AttributeError:
            bye_audio = "http://byeaudiofile"+name
        
        super(self.__class__, self).__init__(name, self.sid, self.token, self.caller_id, self.flow_id)
        self.add_applet(GreetingApplet("hello", hello_audio))
        self.add_applet(GreetingApplet("bye", bye_audio))
    
    def __init__(self, name, hello_audio, bye_audio):
        super(self.__class__, self).__init__(name, self.sid, self.token, self.caller_id, self.flow_id)
        self.add_applet(GreetingApplet("hello", hello_audio))
        self.add_applet(GreetingApplet("bye", bye_audio))

# Code in urls.py
# from django.conf.urls import patterns
# from data_verification import DataVerification
# urlpatterns = patterns('', *HelloBye("hello_bye").urlpatterns())
# urlpatterns = patterns('', *HelloBye("hello_bye_andhra").urlpatterns())