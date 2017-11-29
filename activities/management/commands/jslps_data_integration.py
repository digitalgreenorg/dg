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
        subject = "JSLPS data entry status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['varma.nikhil22@gmail.com']
        # to_email = ['jharkhand@digitalgreen.org', 'system@digitalgreen.org', 'charu@digitalgreen.org']
        body = "Dear Team,\n\n" + "JSLPS data has been successfully updated in COCO.\n\n" + "Here are the details of this update:\n\n" + "Total entries sent by JSLPS (A): " + str(new_count+duplicate_count+other_error_count) + "\nEntries with errors (B): " + str(other_error_count) + "  *e.g. missing video category, missing video in screening, etc. error files are attached.\nEntries we already had (C): " + str(duplicate_count) + "\nEntries successfully updated in COCO (A-(B+C)): " + str(new_count) + "\n\nPlease contact system@digitalgreen.org for any clarification.\n\nThank you.\n"
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in glob.glob("jslps_data_integration_files/*"):
            if files.endswith('.csv'):
                msg.attach_file(files, 'text/csv' )
        msg.send()

    def handle(self, *args, **options): 
        
        print "Geography,jslps_geo"
        call_command('jslps_geo')

        print "Geography,jslps_geo"
        call_command('mksp_jslps_geo')

        print "Groups,jslps_groups"
        call_command('jslps_groups')

        print "Groups,jslps_groups"
        call_command('mksp_jslps_groups')
        
        print "People,jslps_people"
        call_command('jslps_people_new')

        print "People,jslps_people"
        call_command('mksp_jslps_person_new')

        print "Mediators,jslps_mediators"
        call_command('jslps_mediator_new')

        print "Mediators,jslps_mediators"
        call_command('mksp_jslps_mediator_new')

        # print "Videos and Non negotiable,jslps_videos_nn"
        # call_command('jslps_videos_nn_new')
        
        # print "Screening and pma,jslps_screening_pma"
        # call_command('jslps_screening_pma_new')

        # print "MKSP Screening and pma, mksp_jslps_screening_pma"
        # call_command('mksp_jslps_screening_pma')
        
        # print "Adoption,jslps_adoptions"
        # call_command('jslps_adoptions_new')

        self.send_mail()
