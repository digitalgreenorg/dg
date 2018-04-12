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
        to_email = ['jharkhand@digitalgreen.org', 'system@digitalgreen.org', 'charu@digitalgreen.org']
        body = "Dear Team,\n\n" + "JSLPS data has been successfully updated in COCO.\n\n" + "Here are the details of this update:\n\n" + "Total entries sent by JSLPS (A): " + str(new_count+duplicate_count+other_error_count) + "\nEntries with errors (B): " + str(other_error_count) + "  *e.g. missing video category, missing video in screening, etc. error files are attached.\nEntries we already had (C): " + str(duplicate_count) + "\nEntries successfully updated in COCO (A-(B+C)): " + str(new_count) + "\n\nPlease contact system@digitalgreen.org for any clarification.\n\nThank you.\n"
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in glob.glob("jslps_data_integration_files/*"):
            if files.endswith('.csv'):
                msg.attach_file(files, 'text/csv' )
        msg.send()

    def handle(self, *args, **options): 
        
        try:
            print "Geography,jslps_geo"
            call_command('jslps_geo')
        except:
            pass

        try:
            print "Geography,jslps_geo"
            call_command('mksp_jslps_geo')
        except:
            pass

        try:
            print "Groups,jslps_groups"
            call_command('jslps_groups')
        except:
            pass

        try:
            print "Groups,jslps_groups"
            call_command('mksp_jslps_groups')
        except:
            pass
        
        try:
            print "People,jslps_people"
            call_command('jslps_people_new')
        except:
            pass

        try:
            print "People,jslps_people"
            call_command('jslps_people_latest')
        except:
            pass

        try:
            print "People,jslps_people"
            call_command('mksp_jslps_person_new')
        except:
            pass

        try:
            print "Mediators,jslps_mediators"
            call_command('jslps_mediator_new')
        except:
            pass

        try:
            print "Mediators,jslps_mediators"
            call_command('mksp_jslps_mediator_new')
        except:
            pass

        try:
            print "Videos and Non negotiable,jslps_videos_nn"
            call_command('jslps_videos_nn_new')
        except:
            pass

        try:
            print "Videos and Non negotiable,jslps_videos_nn"
            call_command('jslps_videogoatry')
        except:
            pass
        
        try:
            print "Screening and pma,jslps_screening_pma"
            call_command('jslps_screening_pma_new')
        except:
            pass

        try:
            print "MKSP Screening and pma, mksp_jslps_screening_pma"
            call_command('mksp_jslps_screening_pma')
        except:
            pass

        try:
            print "Gotary Screeing"
            call_command('gotary_screening_pma_new')
        except:
            pass
        
        try:
            print "Adoption,jslps_adoptions"
            call_command('jslps_adoptions_new')
        except:
            pass

        
        try:
            print "Health Person"
            call_command('jslps_hnn_person')
        except:
            pass

        
        try:
            print "Health Person New"
            call_command('jslps_hnn_person_new')
        except:
            pass

        
        try:
            print "Health-1"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew1",
                         file_name="jslps-hnn-person-new1.xml", error_file="jslps-hnn-person-new1.csv", file_index=1)
        except:
            pass

        
        try:
            print "Health-2"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew2",
                         file_name="jslps-hnn-person-new2.xml", error_file="jslps-hnn-person-new2.csv", file_index=2)
        except:
            pass

        
        try:
            print "Health-3"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew3",
                         file_name="jslps-hnn-person-new3.xml", error_file="jslps-hnn-person-new3.csv", file_index=3)
        except:
            pass
        
        try:
            print "Health Person New4"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew4",
                         file_name="jslps-hnn-person-new4.xml", error_file="jslps-hnn-person-new4.csv", file_index=4)
        except:
            pass

        try:
            print "Health Person New5"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew5",
                         file_name="jslps-hnn-person-new5.xml", error_file="jslps-hnn-person-new5.csv", file_index=5)
        except:
            pass

        try:
            print "Health Person New6"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew6",
                         file_name="jslps-hnn-person-new6.xml", error_file="jslps-hnn-person-new6.csv", file_index=6)
        except:
            pass

        try:
            print "Health Person New7"
            call_command('jslps_hnn_person_new1', file_url="http://webservicesri.swalekha.in/Service.asmx/GetExportGroupMemberDataHnNNew7",
                         file_name="jslps-hnn-person-new7.xml", error_file="jslps-hnn-person-new7.csv", file_index=6)
        except:
            pass

        self.send_mail()
