from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.mail import EmailMultiAlternatives

import dg.settings

import glob

class Command(BaseCommand):

    def send_mail(self):
        subject = "JSLPS data entry status"
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['aditya@digitalgreen.org', 'vivek@digitalgreen.org', 'vikas@digitalgreen.org', 'abhishekchandran@digitalgreen.org', 'joshin@digitalgreen.org', 'shetty@digitalgreen.org']
        body = "Hi Everyone,\nThis is a automated email after data entry of JSLPS data in database.\nPFA the error files."
        body = "JSLPS data has been inserted in database.\nPFA error files."
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in glob.glob("jslps_data_integration_files/*"):
            if files.endswith('.csv'):
                msg.attach_file(files, 'text/csv' )
        msg.send()

    def handle(self, *args, **options): 

        print "Geography,jslps_geo"
        call_command('jslps_geo')

        print "Groups,jslps_groups"
        call_command('jslps_groups')

        print "People,jslps_people"
        call_command('jslps_people')

        print "Mediators,jslps_mediators"
        call_command('jslps_mediators')

        print "Videos and Non negotiable,jslps_videos_nn"
        call_command('jslps_videos_nn')

        print "Screening and pma,jslps_screening_pma"
        call_command('jslps_screening_pma')
        
        print "Adoption,jslps_adoptions"
        call_command('jslps_adoptions')

        self.send_mail()
    