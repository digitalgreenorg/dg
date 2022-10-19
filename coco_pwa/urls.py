
from django.conf.urls import patterns
from views import service_worker

urlpatterns = patterns('', (r'^sw.js', service_worker))
