from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from dg.base_settings import VIDEOS_PAGE

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=VIDEOS_PAGE)),

)
