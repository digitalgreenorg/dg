from django.conf.urls.defaults import include, patterns, url
from django.views.generic import TemplateView

from communications.views import media_view
from human_resources.views import job_view, member_view
from views import social_home, collection_view, logout_view, partner_view, search_view


class DirectTemplateView(TemplateView):
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context


urlpatterns = patterns('',
    url(r'^$', social_home, name="home"),    
    url(r'^about/$', DirectTemplateView.as_view(template_name='about.html', extra_context={'header':{'jsController':'About', 'currentPage':'About'}}), name='about'),
    url(r'^about/board/$', TemplateView.as_view(template_name='board.html'), name='board'),
    url(r'^about/ourwork/$', TemplateView.as_view(template_name='our_work.html'), name='ourwork'),
    url(r'^about/press/$', media_view, name='press'),
    url(r'^about/reports/1/$', TemplateView.as_view(template_name='annualreport09.html'), name='annualreport09'),
    url(r'^about/reports/1/field$', TemplateView.as_view(template_name='field-developments-09.html'), name='annualreport09fields'),
    url(r'^about/reports/1/learning$', TemplateView.as_view(template_name='learnings-09.html'), name='annualreport09learnings'),
    url(r'^about/resources/$', TemplateView.as_view(template_name='resources.html'), name='resources'),
    url(r'^about/team/$', member_view, name='team'),
    url(r'^about/tools/$', DirectTemplateView.as_view(template_name='tools.html', extra_context={'header': {'currentPage':'Tools'}}), name='tools'),
    url(r'^careers/$', job_view, name='career'),
    url(r'^career/$', job_view),
    # TODO: Connect needs to be fixed.
    url(r'^connect/(?P<partner>.+)/$', partner_view, name='partner'),
    url(r'^connect/$', DirectTemplateView.as_view(template_name='connect.html', extra_context={'header': {'currentPage':'Connect'}}), name='connect'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^discover/(?P<partner>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    url(r'^discover/(?P<partner>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"), 
    url(r'^discover/?$', search_view, name='search'),
    url(r'^discover/$', DirectTemplateView.as_view(template_name='collections.html', extra_context={'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}), name='discover'),
    url(r'^donate/$', TemplateView.as_view(template_name='donate.html'), name='donate'),
    url(r'^example/$', TemplateView.as_view(template_name='example1.html')),
    url(r'^events/$', DirectTemplateView.as_view(template_name='events.html', extra_context={'header':{'jsController':'Events', 'currentPage':'Events'}}), name='events'),
    url(r'^logout/?$', logout_view, name='logout'),
    url(r'^main.js$', TemplateView.as_view(template_name='main.js', content_type='text/javascript'), name='mainjs'),
    # TODO: There are no names used below
    url(r'^press/$', media_view, name='press'),
    url(r'^team/$', member_view, name='team'),
    url(r'^resources/$', TemplateView.as_view(template_name='resources.html'), name='resources'),
    url(r'^tools/$', DirectTemplateView.as_view(template_name='tools.html', extra_context={'header': {'currentPage':'Tools'}}), name='tools'),
)
