from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from communications.views import media_view
from human_resources.views import job_view, member_view, privacy_policy_view
from events import event_registration
from views import social_home, collection_view, partner_view, search_view, collection_add_view, collection_edit_view, video_view, resource_view, picoseekho_view, disseminationprep_view, disseminationform_view, adoptionverification_view

from dg.base_settings import PRODUCT_PAGE

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
    url(r'^$', RedirectView.as_view(url=PRODUCT_PAGE), name="home"),
    #url(r'^$', social_home, name="home"),    
    #url(r'^about/$', DirectTemplateView.as_view(template_name='about.html', extra_context={'header':{'jsController':'About', 'currentPage':'About'}}), name='about'),
    #url(r'^about/board/$', DirectTemplateView.as_view(template_name='board.html', extra_context={'header':{'jsController':'Team', 'currentPage':'Board'}}), name='board'),
    #url(r'^about/ourwork/$', TemplateView.as_view(template_name='our_work.html'), name='ourwork'),
    #url(r'^about/press/$', media_view, name='press'),
    # url(r'^about/training/$', TemplateView.as_view(template_name='training_hi.html'), name='training'),
    # url(r'^about/training/en/$', TemplateView.as_view(template_name='training_en.html'), name='training-el'),
    # url(r'^about/training/hi/$', TemplateView.as_view(template_name='training_hi.html'), name='training-hi'),
    # url(r'^about/training/fr/$', TemplateView.as_view(template_name='training_fr.html'), name='training-fr'),
    #url(r'^about/technology/$', TemplateView.as_view(template_name='technology.html'), name='technology'),
    # url(r'^about/training/picoseekho/(?P<uid>.+)/$', picoseekho_view, name='picoseekho'),
    # url(r'^about/training/picoseekho/$', picoseekho_view, name='picoseekho'),
    # url(r'^about/training/dissemination_prep/(?P<uid>.+)/$', disseminationprep_view, name='disseminationprep'),
    # url(r'^about/training/dissemination_prep/$', disseminationprep_view, name='disseminationprep'),
    # url(r'^about/training/dissemination_form/(?P<uid>.+)/$', disseminationform_view, name='disseminationform'),
    # url(r'^about/training/dissemination_form/$', disseminationform_view, name='disseminationform'),
    # url(r'^about/training/adoption_verification/(?P<uid>.+)/$', adoptionverification_view, name='adoptionverification'),
    # url(r'^about/training/adoption_verification/$', adoptionverification_view, name='adoptionverification'),
    #url(r'^about/reports/1/$', TemplateView.as_view(template_name='annualreport09.html'), name='annualreport09'),
    #url(r'^about/reports/1/field/$', TemplateView.as_view(template_name='field-developments-09.html'), name='annualreport09fields'),
    #url(r'^about/reports/1/learning/$', TemplateView.as_view(template_name='learnings-09.html'), name='annualreport09learnings'),
    #url(r'^about/resources/$', TemplateView.as_view(template_name='resources.html'), name='resources'),
    #url(r'^about/team/$', member_view, name='team'),
    #url(r'^about/privacypolicy', privacy_policy_view, name='privacypolicy'),
    #url(r'^about/tools/$', DirectTemplateView.as_view(template_name='tools.html', extra_context={'header': {'currentPage':'Tools'}}), name='tools'),
    #url(r'^careers/$', job_view, name='career'),
    #url(r'^career/$', job_view),
    # url(r'^collection-add/(?P<collection>.+)/$', collection_edit_view, name='edit_collection'),
    # url(r'^collection-add/$', collection_add_view, name='create_collection'),
    #url(r'^connect/usaid-ind/$', TemplateView.as_view(template_name='usaid.html'), name='usaid'),
    #url(r'^connect/usaid-dlec/$', DirectTemplateView.as_view(template_name='dlec.html', extra_context={'header': {'jsController':'Home'}}), name='dlec'),
    #url(r'^connect/usaid-eth/$', DirectTemplateView.as_view(template_name='usaid_eth.html', extra_context={'header': {'jsController':'Home'}}), name='usaid-eth'),
    #url(r'^connect/(?P<partner>.+)/$', partner_view, name='partner'),
    #url(r'^connect/$', DirectTemplateView.as_view(template_name='connect.html', extra_context={'header': {'currentPage':'Connect', 'jsController':'Connect'}}), name='connect'),
    #url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    #url(r'^discover/video/(?P<uid>.+)/$', video_view, name="video_page"),
    #url(r'^discover/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/(?P<video>\d+)/$', collection_view, name="collection_video_page"), 
    #url(r'^discover/(?P<partner>.+)/(?P<country>.+)/(?P<state>.+)/(?P<language>.+)/(?P<title>.+)/$', collection_view, name="collection_page"),     
    #url(r'^discover/?$', search_view, name='search'),
    #url(r'^discover/$', DirectTemplateView.as_view(template_name='collections.html', extra_context={'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}), name='discover'),
    #url(r'^donate/$', TemplateView.as_view(template_name='donate.html'), name='donate'),
    #url(r'^example/$', TemplateView.as_view(template_name='example1.html')),
    #url(r'^events/$', DirectTemplateView.as_view(template_name='events.html', extra_context={'header':{'jsController':'Events', 'currentPage':'Events'}}), name='events'),
    #url(r'^events/registration/$', event_registration, name='event_registration'),
    url(r'^main.js$', TemplateView.as_view(template_name='main.js', content_type='text/javascript'), name='mainjs'),
    #url(r'^press/$', media_view, name='press'),
    #url(r'^resources/annual_reports/$', TemplateView.as_view(template_name='annual_reports.html'), name='annual_reports'),
    #url(r'^resources/our_programs/$', TemplateView.as_view(template_name='our_programs.html'), name='our_programs'),
    #url(r'^resources/field_stories/$', TemplateView.as_view(template_name='field_stories.html'), name='field_stories'),
    #url(r'^resources/sop/$', TemplateView.as_view(template_name='sop.html'), name='sop'),
    #url(r'^resources/qa/$', TemplateView.as_view(template_name='qa_resource.html'), name='qa-resource'),
    #url(r'^resources/research/$', TemplateView.as_view(template_name='research.html'), name='research'),
    #url(r'^resources/dlec/reports/$', TemplateView.as_view(template_name='dlec_resource.html'), name='dlec-resource'),
    #url(r'^resources/posters/$', TemplateView.as_view(template_name='posters.html'), name='posters'),
    #url(r'^resources/(?P<uid>.+)/$', resource_view, name='resources'),
    #url(r'^resources/$', resource_view, name='resources'),
    #url(r'^sitemap/$', TemplateView.as_view(template_name='sitemap.html'), name='sitemap'),
    #url(r'^team/$', member_view, name='team'),
    #url(r'^tools/$', DirectTemplateView.as_view(template_name='tools.html', extra_context={'header': {'currentPage':'Tools'}}), name='tools'),
)
