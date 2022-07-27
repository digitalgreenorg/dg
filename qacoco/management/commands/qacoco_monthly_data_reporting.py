from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

import pandas as pd
import pandas.io.sql as psql
import MySQLdb
import dg.settings
import csv
import datetime

class Command(BaseCommand):

    def send_mail(self,attached_files):
        till_date = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = "QA COCO: Data as of %s"%(till_date)
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['eth_qacoco_monthly_report_recipients@digitalgreen.org']
        body = "Dear Team,\n\nPlease find the attached QA COCO data entered as of %s.\nYou may reach out to system@digitalgreen.org for any question or clarification.\n\nThank you."%(till_date)
        msg = EmailMessage(subject, body, from_email, to_email)
        for file in attached_files:
            msg.attach_file(file, 'text/csv' )
        msg.send()

    def run_query(self,query):
        mysql_cn = MySQLdb.connect(host=dg.settings.DATABASES['default']['HOST'], port=dg.settings.DATABASES['default']['PORT'], 
            user=dg.settings.DATABASES['default']['USER'] ,
            passwd=dg.settings.DATABASES['default']['PASSWORD'],
            db=dg.settings.DATABASES['default']['NAME'],
            charset = 'utf8',
            use_unicode = True)
        temp_df = psql.read_sql(query, con=mysql_cn)
        mysql_cn.close()
        return temp_df

    def handle(self, *args, **options):

        file_save_path = "qacoco/files/"
        video_quality_query = '''
            SELECT 
                YEAR(qr.date) Year,
                MONTHNAME(qr.date) Month,
                gc.country_name Country,
                gs.state_name State,
                gd.DISTRICT_NAME District,
                gb.BLOCK_NAME Block,
                gv.id 'Village Id',
                gv.VILLAGE_NAME Village,
                qr.date Date,
                vv.id 'Video ID',
                vv.title 'Video Title',
                qr.storystructure 'Story Structure',
                qr.framing 'Framing',
                qr.continuity 'Continuity',
                qr.camera_angles 'Camera Angles',
                qr.camera_movement 'Camera Movement',
                qr.light 'Light',
                qr.audio_sound 'Audio Sound',
                qr.editing 'Editing',
                qr.intro_and_importance 'Into and Importance',
                qr.facilitation 'Facilitation',
                qr.non_negotiable_pts 'Non Negotiable Points',
                qr.story_board 'Story Board',
                qr.ease_of_understanding 'Ease of Understanding',
                qr.gender_sensitivity 'Gender Sensitivity',
                qr.total_score 'Total Score',
                qr.video_grade 'Video Grade',
                qr.total_score 'Total Score',
                qr.video_grade 'Video Grade',
                CASE qr.approval
                    WHEN '1' THEN 'Yes'
                    WHEN '0' THEN 'No'
                END 'Approve for Dissemination',
                vn.id 'Reviewer Id',
                vn.name 'Reviewed By',
                qr.remarks 'Remarks',
                au.username 'Created By'
            FROM
                qacoco_videoqualityreview qr
                    JOIN
                videos_video vv ON vv.id = qr.video_id
                    JOIN
                geographies_village gv ON gv.id = vv.village_id
                    JOIN
                geographies_block gb ON gb.id = gv.block_id
                    JOIN
                geographies_district gd ON gd.id = gb.district_id
                    JOIN
                geographies_state gs ON gs.id = gd.state_id
                    JOIN
                geographies_country gc ON gc.id = gs.country_id
                    JOIN
                qacoco_qareviewername vn ON vn.id = qr.qareviewername_id
                    JOIN
                auth_user au ON qr.user_created_id = au.id
            ORDER BY qr.date DESC
        '''

        dissemination_quality_query = '''
            SELECT 
                YEAR(qd.date) Year,
                MONTHNAME(qd.date) Month,
                gc.country_name Country,
                gs.state_name State,
                gd.DISTRICT_NAME District,
                gb.BLOCK_NAME Block,
                gv.id 'Village Id',
                gv.VILLAGE_NAME Village,
                pg.group_name 'Group Name',
                qd.date Date,
                vv.id 'Video ID',
                vv.title 'Video Title',
                pa.id AS 'Mediator Id',
                pa.name AS 'Mediator',
                CASE qd.pico
                    WHEN '1' THEN 'Working'
                    WHEN '0' THEN 'Not Working'
                END 'Pico',
                CASE qd.speaker
                    WHEN '1' THEN 'Working'
                    WHEN '0' THEN 'Not Working'
                END 'Speaker',
                CASE qd.remote
                    WHEN '1' THEN 'Working'
                    WHEN '0' THEN 'Not Working'
                END 'Remote',
                qd.equipments_setup_handling 'Equipment Setup',
                qd.maintained_ideal_darkness 'Maintained Ideal Darkness',
                qd.maintained_ideal_screen_size 'Maintained Ideal Screen Size',
                qd.maintained_ideal_av_quality 'Maintained Ideal AV Quality',
                qd.established_logical_conn 'Established Logical Connection',
                qd.introduce_topic 'Introduced Topic',
                qd.paused_video 'Paused Video',
                qd.encouraged_adoption 'Encouraged Adoption',
                qd.summarized_video 'Summarized Video',
                qd.subject_knowledge 'Subject Knowledge',
                qd.filled_dissemination 'Filled Dissemination',
                qd.total_score 'Total Score',
                qd.video_grade 'Video Grade',
                vn.id 'Reviewer Id',
                vn.name AS 'Reviewed By',
                qd.remark 'Remarks',
                au.username 'Created By'
            FROM
                qacoco_disseminationquality qd
                    JOIN
                videos_video vv ON vv.id = qd.video_id
                    JOIN
                qacoco_qareviewername vn ON vn.id = qd.qareviewername_id
                    JOIN
                people_animator pa ON pa.id = qd.mediator_id
                    JOIN
                people_persongroup pg ON pg.id = qd.group_id
                    JOIN
                geographies_village gv ON gv.id = qd.village_id
                    JOIN
                geographies_block gb ON gb.id = gv.block_id
                    JOIN
                geographies_district gd ON gd.id = gb.district_id
                    JOIN
                geographies_state gs ON gs.id = gd.state_id
                    JOIN
                geographies_country gc ON gc.id = gs.country_id
                    JOIN
                auth_user au ON qd.user_created_id = au.id
            ORDER BY qd.date DESC
        '''

        adoption_verification_query = '''
            SELECT 
                af.id 'af_id',
                YEAR(af.verification_date) Year,
                MONTHNAME(af.verification_date) Month,
                gc.country_name Country,
                gs.state_name State,
                gd.DISTRICT_NAME District,
                gb.BLOCK_NAME Block,
                gv.id 'Village Id',
                gv.VILLAGE_NAME Village,
                af.verification_date 'Verification Date',
                vv.id 'Video ID',
                vv.title 'Video Title',
                pp.id 'Person ID',
                pp.person_name AS 'Person Name',
                pa.id AS 'Mediator Id',
                pa.name AS 'Mediator',
                vn.id AS 'Reviewer Id',
                vn.name AS 'Reviewed By',
                au.username 'Created By'
            FROM
                qacoco_adoptionverification af
                    JOIN
                videos_video vv ON vv.id = af.video_id
                    JOIN
                qacoco_qareviewername vn ON vn.id = af.qareviewername_id
                    JOIN
                people_animator pa ON pa.id = af.mediator_id
                    JOIN
                people_person pp ON pp.id = af.person_id
                    JOIN
                geographies_village gv ON gv.id = af.village_id
                    JOIN
                geographies_block gb ON gb.id = gv.block_id
                    JOIN
                geographies_district gd ON gd.id = gb.district_id
                    JOIN
                geographies_state gs ON gs.id = gd.state_id
                    JOIN
                geographies_country gc ON gc.id = gs.country_id
                    JOIN
                auth_user au ON au.id = af.user_created_id
            ORDER BY YEAR(af.verification_date) DESC , MONTH(af.verification_date) DESC
        '''

        adoption_verification_nonnego_query = '''
            SELECT 
                af.id 'af_id',
                GROUP_CONCAT(IF(ann.adopted = '1', 'Yes', 'No')) 'Non Negotiable Adopted'
            FROM
                qacoco_adoptionverification af
                    JOIN
                qacoco_adoptionnonnegotiableverfication ann ON af.id = ann.adoptionverification_id
            GROUP BY af.id
        '''

        # Run the individual queries and put them on a variable
        video_quality_df = self.run_query(video_quality_query)
        dissemination_quality_df = self.run_query(dissemination_quality_query)
        adoption_verification_df = self.run_query(adoption_verification_query)
        adoption_verification_nonnego_df = self.run_query(adoption_verification_nonnego_query)

        # JOIN the adoption verification and adopted non negotiables
        combine_df = pd.merge(adoption_verification_df, adoption_verification_nonnego_df, how='inner')
        combine_df = combine_df.drop('af_id', axis=1)

        # Save the results on a CSV file
        video_quality_df.to_csv(file_save_path+"video_quality_review.csv", sep=',', encoding='utf-8', index=False)
        dissemination_quality_df.to_csv(file_save_path+"dissemination_quality.csv", sep=',', encoding='utf-8', index=False)
        combine_df.to_csv(file_save_path+"adoption_verification.csv", sep=',', encoding='utf-8', index=False)

        # Attach and send them via email
        self.send_mail([file_save_path+"video_quality_review.csv",file_save_path+"dissemination_quality.csv",file_save_path+"adoption_verification.csv"])
