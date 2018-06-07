from django.core.management.base import BaseCommand, CommandError
from loop.models import Farmer, Gaddidar, Transporter, Language

from googletrans import Translator


class Command(BaseCommand):
    help = '''This command converts hindi text to english using googletrans api. (http://py-googletrans.readthedocs.io/en/latest/)'''

    translator = Translator()

    def add_arguments(self, parser):
        parser.add_argument('-t',
                            dest='table',
                            default='Farmer')

    def translate_text(self, text):
        eng_text = self.translator.translate(text, src='hi', dest='en')
        return eng_text

    def handle(self, *args, **options):
        print("Start")
        if options.get('table') == 'farmer':
            #L.assigned_villages()
            farmer_list = Farmer.objects.filter(village__block__district__state=1)
            print farmer_list.count()
            for farmer in farmer_list:
                farmer.farmer_name_en = self.translate_text(farmer.name).text
                farmer.save()

        if options.get('table') == 'transporter':
            transporter_list = Transporter.objects.filter(block__district__state=1)
            print transporter_list.count()
            for transporter in transporter_list:
                transporter.transporter_name_en = self.translate_text(transporter.transporter_name).text
                transporter.save()

