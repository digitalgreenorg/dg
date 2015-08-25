from django.conf.urls import include, patterns, url
from exotel import ExotelService
from applets import GreetingApplet

# url of a greeting audio is /ivrs/service_name/applet_name/

#TODO some of these must come from settings
sid = "digitalgreen2"
token = "421c11b1235067ca30ca87590c80c31eadc46af0"
caller_id="01130018178"
flow_id = "27037"

hello_bye_andhra = ExotelService("hello", sid, token, caller_id, flow_id)
hello_bye_andhra.add_applet(GreetingApplet("h", "http://helloandhraaudiofile2"))


services = []
services.extend(hello_bye_andhra.urlpatterns())
# To add a service add the call the urlpatterns of the service over here

urlpatterns = patterns('', 
    *(services)
)
