from exotel import ExotelService
from applets import GreetingApplet

class HelloBye(ExotelService):
    name = "hello_bye"
    #TODO some of these must come from settings
    sid = "digitalgreen2"
    token = "421c11b1235067ca30ca87590c80c31eadc46af0"
    caller_id="01130018178"
    flow_id = "27037"
    applets = {
        'hello': GreetingApplet("http://helloaudiofile"),
        'bye': GreetingApplet("http://byeaudiofile"),
    } 

# Code in urls.py
# from django.conf.urls import patterns
# from data_verification import DataVerification
# urlpatterns = patterns('', *HelloBye("hello_bye").urlpatterns())
# urlpatterns = patterns('', *HelloBye("hello_bye_andhra").urlpatterns())