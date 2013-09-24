from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from dashboard.models import District, PersonAdoptPractice, Video


class CustomFeedGenerator(Atom1Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"georss:point", item['georss:point'])
        handler.addQuickElement(u"dgrss:adoptionQuantity", item['dgrss:adoptionQuantity'])
        handler.addQuickElement(u"dgrss:sector", item['dgrss:sector'])
        handler.addQuickElement(u"dgrss:subsector", item['dgrss:subsector'])
        handler.addQuickElement(u"dgrss:topic", item['dgrss:topic'])
        handler.addQuickElement(u"dgrss:subtopic", item['dgrss:subtopic'])
        handler.addQuickElement(u"dgrss:subject", item['dgrss:subject'])
        handler.addQuickElement(u"dgrss:analyticsLink", item['dgrss:analyticsLink'])

class DistrictFeed(Feed):
    feed_type = CustomFeedGenerator
    title = "Digital Green Data Feed"
    subtitle = ""
    link = "http://www.digitalgreen.org"
    author_name = 'Aadish Gupta'
    author_email = 'aadish@digitalgreen.org'

    def items(self):
        return District.objects.all()

    def item_title(self, item):
        return item.district_name

    def item_link(self, item):
        return ''.join(['http://www.digitalgreen.org/analytics/overview_module?geog=district&id=', str(item.id)])

    def item_extra_kwargs(self, item):

        adoptionQuantity = PersonAdoptPractice.objects.filter(person__village__block__district__id = item.id).count()
        sector_list = filter(None,Video.objects.filter(village__block__district__id=item.id).values_list('related_practice__practice_sector__name', flat='true').distinct())
        subsector_list = filter(None,Video.objects.filter(village__block__district__id=item.id).values_list('related_practice__practice_subsector__name', flat='true').distinct())
        topic_list = filter(None,Video.objects.filter(village__block__district__id=item.id).values_list('related_practice__practice_topic__name', flat='true').distinct())
        subtopic_list = filter(None,Video.objects.filter(village__block__district__id=item.id).values_list('related_practice__practice_subtopic__name', flat='true').distinct())
        subject_list = filter(None,Video.objects.filter(village__block__district__id=item.id).values_list('related_practice__practice_subject__name', flat='true').distinct())

        return {
                 'georss:point': ' '.join([item.latitude, item.longitude]),
                 'dgrss:adoptionQuantity': str(adoptionQuantity),
                 'dgrss:sector': ', '.join(sector_list),
                 'dgrss:subsector': ', '.join(subsector_list),
                 'dgrss:topic': ', '.join(topic_list),
                 'dgrss:subtopic': ', '.join(subtopic_list),
                 'dgrss:subject': ', '.join(subject_list),
                 'dgrss:analyticsLink': ''.join(['http://www.digitalgreen.org/analytics/overview_module?geog=district&id=', str(item.id)]),
                 }
