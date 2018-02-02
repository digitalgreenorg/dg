from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import EmailMultiAlternatives
import dg.settings
import glob

new_count = 0
duplicate_count = 0
other_error_count = 0

class Command(BaseCommand):

    def send_mail(self):
        subject = "AP data entry status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['varma.nikhil22@gmail.com']
        # to_email = ['jharkhand@digitalgreen.org', 'system@digitalgreen.org', 'charu@digitalgreen.org']
        body = "Dear Team,\n\n" + "AP data has been successfully updated in COCO.\n\n" + "Here are the details of this update:\n\n" + "Total entries sent by JSLPS (A): " + str(new_count+duplicate_count+other_error_count) + "\nEntries with errors (B): " + str(other_error_count) + "  *e.g. missing video category, missing video in screening, etc. error files are attached.\nEntries we already had (C): " + str(duplicate_count) + "\nEntries successfully updated in COCO (A-(B+C)): " + str(new_count) + "\n\nPlease contact system@digitalgreen.org for any clarification.\n\nThank you.\n"
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in glob.glob("ap/*"):
            if files.endswith('.csv'):
                msg.attach_file(files, 'text/csv' )
        msg.send()

    def handle(self, *args, **options): 
        
        print "Geography,ap_geo"
        call_command('bluefrog_geo')
        
        # print "People,ap_people"
        # call_command('bluefrog_person')

        # print "Mediators,ap_mediators"
        # call_command('bluefrog_mediator')

        # print "Subcategory,ap_crops"
        # call_command('bluefrog_crops')

        # print "Practice, ap_pest_management"
        # call_command('bluefrog_practice')

        # print "Practice, ap_fertility_management"
        # call_command('bluefrog_practice_new')

        # print "Screening, ap_screening"
        # call_command('bluefrog_screening')

        # print "Adoption, ap_adoption"
        # call_command('bluefrog_adoptions')


        self.send_mail()
