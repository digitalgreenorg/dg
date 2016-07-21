from django.conf.urls import include, patterns, url
from hello_bye import HelloBye
from jharkhand_pilot import JharkhandPilot
from ivr_baatcheet import IvrBaatcheet

# url of a greeting audio is /ivrs/service_name/applet_name/

# #TODO some of these must come from settings
# sid = "digitalgreen2"
# token = "421c11b1235067ca30ca87590c80c31eadc46af0"
# caller_id="01130018178"
# flow_id = "27037"
# views =
#
# hello_bye_andhra = ExotelService("hello", sid, token, caller_id, flow_id)
# hello_bye_andhra.add_applet(GreetingApplet("h", "http://helloandhraaudiofile2"))

services = []

hello = HelloBye()
services.extend(hello.urlpatterns())
ivrbaatcheet = IvrBaatcheet()
services.extend(ivrbaatcheet.urlpatterns())
jharkhand_pilot = JharkhandPilot()
services.extend(jharkhand_pilot.urlpatterns())

greeting = HelloBye(name="greeting")
# class Greeting(HelloBye):
# 	name="greeting"
services.extend(greeting.urlpatterns())
#print services

# To add a service add the call the urlpatterns of the service over here
urlpatterns = patterns('', 
    *(services)
)

# TODO
# Code up models
# Migrate models
# Test state models
# Test harness
