from django.conf.urls import include, patterns, url
from exotel import ExotelService
from applets import GreetingApplet

service_name = "hello_bye"
#TODO some of these must come from settings
sid = "digitalgreen2"
token = "421c11b1235067ca30ca87590c80c31eadc46af0"
caller_id="01130018178"
flow_id = "27037"

hello_bye_andhra = ExotelService("hello_bye_andhra", sid, token, caller_id, flow_id)
hello_bye_andhra.add_applet(GreetingApplet("hello", "http://helloandhraaudiofile2"))
hello_bye_andhra.add_applet(GreetingApplet("bye", "http://byeandhraaudiofile2"))

hello_bye_service = ExotelService(service_name, sid, token, caller_id, flow_id)
# url of a greeting audio is /ivrs/service_name/applet_name/

hello_bye_service.add_applet(GreetingApplet("hello", "http://helloaudiofile1"))
hello_bye_service.add_applet(GreetingApplet("bye", "http://byeaudiofile1"))

#urlpatterns = patterns('', *(hello_bye_service.urlpatterns()+hello_bye_andhra.urlpatterns()))
urlpatterns = patterns('', *(hello_bye_andhra.urlpatterns()+hello_bye_service.urlpatterns()))
#, *)
    #],
#)
