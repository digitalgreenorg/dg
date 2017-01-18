from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from qacoco.models import *

import dg.settings
import csv
import datetime

class Command(BaseCommand):

    def make_csv(self,csv_headers,csv_data,reporting_file_path):

        with open(reporting_file_path,'wb') as final_output:
            dict_writer = csv.DictWriter(final_output,csv_headers)
            dict_writer.writeheader()
            dict_writer.writerows(csv_data)

    def send_mail(self,attached_files):
        till_date = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = "QA COCO: Data received till %s"%(till_date)
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['system@digitalgreen.org', 'swati@digitalgreen.org', 'kaushik@digitalgreen.org', 'aditya@digitalgreen.org', 'vivek@digitalgreen.org', 'vikas@digitalgreen.org', 'abhishekchandran@digitalgreen.org']
        body = "Dear Team,\n\nPlease find the attached QA COCO data entered till %s.\nPlease contact system@digitalgreen.org for any question or clarification.\n\nThank you."%(till_date)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in attached_files:
            msg.attach_file(files, 'text/csv' )
        msg.send()

    def utf_8(self,obj):
        return str(obj.encode('utf-8'))

    def handle(self, *args, **options): 

        months_dic = dict(January=1, February=2, March=3, April=4, May=5, June=6, July=7,
              August=8, September=9, October=10, November=11, December=12)
        file_save_path = "qacoco/files/"
        
        video_quality_data = []
        video_quality_review = VideoQualityReview.objects.filter(date__isnull=False).select_related('video', 'qareviewername')
        for review_entry in video_quality_review:
            year = str(review_entry.date.strftime('%Y'))
            month = str(review_entry.date.strftime('%B'))
            video_id = review_entry.video_id
            video_title = review_entry.video.title
            reviewer_name = review_entry.qareviewername.name
            approved = "Yes" if review_entry.approval == '1' else "No"
            user_created = str(review_entry.user_created.username)
            video_quality_data.append({'Year':year, 'Month':month, 'Date':review_entry.date, 'Video ID':video_id, 'Video Title':video_title, 'Story Structure':review_entry.storystructure, 'Framing':review_entry.framing, 'Continuity':review_entry.continuity, 'Camera Angles':review_entry.camera_angles, 'Camera Movement':review_entry.camera_movement, 'Light':review_entry.light, 'Audio and Sound':review_entry.audio_sound, 'Interview':review_entry.interview, 'Technical':review_entry.technical, 'Style Guide':review_entry.style_guide, 'Total Score':review_entry.total_score, 'Video Grade':review_entry.video_grade, 'Approve for Dissemination':approved, 'Reviewed By':reviewer_name, 'Remarks':review_entry.remarks, 'Created By':user_created})
        del video_quality_review
        video_quality_data = sorted(video_quality_data,key=lambda ele: (ele['Year'],months_dic[ele['Month']]),reverse=True)
        csv_headers = ['Year', 'Month', 'Date', 'Video ID', 'Video Title', 'Story Structure', 'Framing', 'Continuity', 'Camera Angles', 'Camera Movement', 'Light', 'Audio and Sound', 'Interview', 'Technical', 'Style Guide', 'Total Score', 'Video Grade', 'Approve for Dissemination', 'Reviewed By', 'Remarks', 'Created By']
        self.make_csv(csv_headers,video_quality_data,file_save_path+"video_quality_review.csv")
        del video_quality_data

        dissemination_quality_data = []
        dissemination_quality = DisseminationQuality.objects.filter(date__isnull=False).select_related('village', 'mediator', 'video','qareviewername')
        for entry in dissemination_quality:
            year = str(entry.date.strftime('%Y'))
            month = str(entry.date.strftime('%B'))
            video_id = entry.video_id
            video_title = self.utf_8(entry.video.title)
            reviewer_name = self.utf_8(entry.qareviewername.name)
            mediator_name = self.utf_8(entry.mediator.name)
            pico_working = "Working" if entry.pico == '1' else "Not Working"
            speaker_working = "Working" if entry.speaker == '1' else "Not Working"
            country = self.utf_8(entry.village.block.district.state.country.country_name)
            state = self.utf_8(entry.village.block.district.state.state_name)
            district = self.utf_8(entry.village.block.district.district_name)
            block = self.utf_8(entry.village.block.block_name)
            village = self.utf_8(entry.village.village_name)
            user_created = str(entry.user_created.username)
            dissemination_quality_data.append({'Year':year, 'Month':month, 'Country':country, 'State':state, 'District':district, 'Block':block, 'Village':village, 'Date':entry.date, 'Video ID':video_id, 'Video Title':video_title, 'Mediator':mediator_name, 'Pico':pico_working, 'Speaker':speaker_working, 'Equipments setup handling':entry.equipments_setup_handling, 'context_setting':entry.context_setting, 'Topic Introduction':entry.introduce_topic, 'Paused video at important places':entry.paused_video, 'Encouraged for Adoption':entry.encouraged_adoption, 'Summarized Video':entry.summarized_video, 'Subject knowledge':entry.subject_knowledge, 'Filled Dissemination':entry.filled_dissemination, 'Total Score':entry.total_score, 'Video Grade':entry.video_grade, 'Reviewed By':reviewer_name, 'Remarks':entry.remark, 'Created By':user_created})
        del dissemination_quality
        dissemination_quality_data = sorted(dissemination_quality_data,key=lambda ele: (ele['Year'],months_dic[ele['Month']],ele['Country'],ele['State'],ele['District'],ele['Block'],ele['Village']),reverse=True)
        csv_headers = ['Year', 'Month', 'Country', 'State', 'District', 'Block', 'Village', 'Date', 'Video ID', 'Video Title', 'Mediator', 'Pico', 'Speaker', 'Equipments setup handling', 'context_setting', 'Topic Introduction', 'Paused video at important places', 'Encouraged for Adoption', 'Summarized Video', 'Subject knowledge', 'Filled Dissemination', 'Total Score', 'Video Grade', 'Reviewed By', 'Remarks', 'Created By']
        self.make_csv(csv_headers,dissemination_quality_data,file_save_path+"dissemination_quality.csv")
        del dissemination_quality_data
        
        adoption_verification_data = []
        non_nego_adopted = {}
        adoption_verification = AdoptionVerification.objects.filter(verification_date__isnull=False).select_related('village','mediator','person','video','qareviewername')
        adoption_nonnego_verification = AdoptionNonNegotiableVerfication.objects.all()
        for entry in adoption_verification:
            year = str(entry.verification_date.strftime('%Y'))
            month = str(entry.verification_date.strftime('%B'))
            video_id = entry.video_id
            video_title = self.utf_8(entry.video.title)
            reviewer_name = self.utf_8(entry.qareviewername.name)
            mediator_name = self.utf_8(entry.mediator.name)
            person_id = entry.person_id
            person_name = entry.person.person_name
            country = self.utf_8(entry.village.block.district.state.country.country_name)
            state = self.utf_8(entry.village.block.district.state.state_name)
            district = self.utf_8(entry.village.block.district.district_name)
            block = self.utf_8(entry.village.block.block_name)
            village = self.utf_8(entry.village.village_name)
            user_created = str(entry.user_created.username)
            nonnego_adopted = adoption_nonnego_verification.filter(adoptionverification=entry)
            non_nego_adopted['n1_adopted'] = non_nego_adopted['n2_adopted'] = non_nego_adopted['n3_adopted'] = non_nego_adopted['n4_adopted'] = non_nego_adopted['n5_adopted'] = "N/A"
            for index in range(len(nonnego_adopted)):
                non_nego = "n"+str(index+1)+"_adopted"
                non_nego_adopted[non_nego] = "Yes" if nonnego_adopted[index].adopted else "No"
            adoption_verification_data.append({'Year':year, 'Month':month, 'Country':country, 'State':state, 'District':district, 'Block':block, 'Village':village, 'Verification Date':entry.verification_date, 'Video ID':video_id, 'Video Title':video_title, 'Person ID':person_id, 'Person Name':person_name,'Mediator':mediator_name, 'Reviewed By':reviewer_name, 'n1 Adopted ?':non_nego_adopted['n1_adopted'], 'n2 Adopted ?':non_nego_adopted['n2_adopted'], 'n3 Adopted ?':non_nego_adopted['n3_adopted'], 'n4 Adopted ?':non_nego_adopted['n4_adopted'], 'n5 Adopted ?':non_nego_adopted['n5_adopted'], 'Created By':user_created})
        del adoption_verification
        adoption_verification_data = sorted(adoption_verification_data,key=lambda ele: (ele['Year'],months_dic[ele['Month']],ele['Country'],ele['State'],ele['District'],ele['Block'],ele['Village']),reverse=True)
        csv_headers = ['Year', 'Month', 'Country', 'State', 'District', 'Block', 'Village', 'Verification Date', 'Video ID', 'Video Title', 'Person ID', 'Person Name', 'Mediator', 'Reviewed By', 'n1 Adopted ?', 'n2 Adopted ?', 'n3 Adopted ?', 'n4 Adopted ?', 'n5 Adopted ?', 'Created By']
        self.make_csv(csv_headers,adoption_verification_data,file_save_path+"adoption_verification.csv")
        del adoption_verification_data

        #self.send_mail([file_save_path+"video_quality_review.csv",file_save_path+"dissemination_quality.csv",file_save_path+"adoption_verification.csv"])
