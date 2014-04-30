from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from geographies.models import District 
from activities.models import PersonAdoptPractice
from videos.models import  Video


class CombinedCustomFeedGenerator(Atom1Feed):
    def add_item_elements(self, handler, item):
        super(CombinedCustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"georss:point", item['georss:point'])


class IndividualCustomFeedGenerator(Atom1Feed):
    def add_item_elements(self, handler, item):
        super(IndividualCustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"georss:point", item['georss:point'])
        handler.addQuickElement(u"dgrss:adoptionQuantity", item['dgrss:adoptionQuantity'])
        handler.addQuickElement(u"dgrss:sector", item['dgrss:sector'])
        handler.addQuickElement(u"dgrss:subsector", item['dgrss:subsector'])
        handler.addQuickElement(u"dgrss:topic", item['dgrss:topic'])
        handler.addQuickElement(u"dgrss:subtopic", item['dgrss:subtopic'])
        handler.addQuickElement(u"dgrss:subject", item['dgrss:subject'])
        handler.addQuickElement(u"dgrss:analyticsLink", item['dgrss:analyticsLink'])
        handler.addQuickElement(u"dgrss:videosLink", item['dgrss:videosLink'])


class CombinedDistrictFeed(Feed):
    feed_type = CombinedCustomFeedGenerator
    title = "Digital Green All Districts"
    subtitle = "All Districts ID, Name and Geo-Co-ordinates"
    link = "http://www.digitalgreen.org"
    author_name = 'Aadish Gupta'
    author_email = 'aadish@digitalgreen.org'

    def items(self):
        return District.objects.all()

    def item_title(self, item):
        return item.district_name

    def item_link(self, item):
        return ''.join(['http://www.digitalgreen.org/analytics/overview_module?geog=district&id=', str(item.id)])

    def item_guid(self, item):
        return str(item.id)

    def item_extra_kwargs(self, item):
        return {
                 'georss:point': ' '.join([str(item.latitude), str(item.longitude)]),
                 }


class IndividualDistrictFeed(Feed):
    feed_type = IndividualCustomFeedGenerator
    title = "Digital Green Data Feed"
    subtitle = " District with practices, sub-practices, topic, sub-topic, subject"
    link = "http://www.digitalgreen.org"
    author_name = 'Aadish Gupta'
    author_email = 'aadish@digitalgreen.org'

    def get_object(self, request, district_id):
        return get_object_or_404(District, pk=district_id)

    def items(self, obj):
        return District.objects.filter(id=obj.id)

    def item_title(self, item):
        return item.district_name

    def item_link(self, item):
        return ''.join(['http://www.digitalgreen.org/analytics/overview_module?geog=district&id=', str(item.id)])

    def item_extra_kwargs(self, item):
        adoption_list = PersonAdoptPractice.objects.filter(person__village__block__district__id = item.id)
        adoption_quantity = adoption_list.count()
        sector_list = filter(None, adoption_list.values_list('video__related_practice__practice_sector__name', flat='true').distinct())
        subsector_list = filter(None, adoption_list.values_list('video__related_practice__practice_subsector__name', flat='true').distinct())
        topic_list = filter(None, adoption_list.values_list('video__related_practice__practice_topic__name', flat='true').distinct())
        subtopic_list = filter(None, adoption_list.values_list('video__related_practice__practice_subtopic__name', flat='true').distinct())
        subject_list = filter(None, adoption_list.values_list('video__related_practice__practice_subject__name', flat='true').distinct())
        state = item.state.state_name.replace(' ', '%20')
        return {
                 'georss:point': ' '.join([str(item.latitude), str(item.longitude)]),
                 'dgrss:adoptionQuantity': str(adoption_quantity),
                 'dgrss:sector': ', '.join(sector_list),
                 'dgrss:subsector': ', '.join(subsector_list),
                 'dgrss:topic': ', '.join(topic_list),
                 'dgrss:subtopic': ', '.join(subtopic_list),
                 'dgrss:subject': ', '.join(subject_list),
                 'dgrss:analyticsLink': ''.join(['http://www.digitalgreen.org/analytics/overview_module?geog=district&id=', str(item.id)]),
                 'dgrss:videosLink': ''.join(['http://www.digitalgreen.org/discover/?searchString=', state])
                 }
