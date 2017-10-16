from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

import pandas as pd
import pandas.io.sql as psql
import MySQLdb
import dg.settings
import csv
import datetime

class Command(BaseCommand):

    def send_mail(self,attached_files):
        till_date = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = "QA COCO: Data till %s"%(till_date)
        from_email = dg.settings.EMAIL_HOST_USER
        to_email = ['all@digitalgreen.org']
        body = "Dear Team,\n\nPlease find attached QA COCO data entered till %s.\nPlease contact system@digitalgreen.org for any question or clarification.\n\nThank you."%(till_date)
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for files in attached_files:
            msg.attach_file(files, 'text/csv' )
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
        video_quality_query = '''SELECT
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
                qr.storystructure,
                qr.framing,
                qr.camera_angles,
                qr.camera_movement,
                qr.light,
                qr.audio_sound,
                qr.continuity,
                qr.interview,
                qr.technical,
                qr.style_guide 'Style Guide',
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
            GROUP BY YEAR(qr.date) , MONTH(qr.date) , gc.id , gs.id , gd.id , gb.id , gv.id , vv.id
            ORDER BY YEAR(qr.date) DESC , MONTH(qr.date) DESC
        '''

        dissemination_quality_query = '''SELECT
            YEAR(qd.date) Year,
            MONTHNAME(qd.date) Month,
            gc.country_name Country,
            gs.state_name State,
            gd.DISTRICT_NAME District,
            gb.BLOCK_NAME Block,
            gv.id 'Village Id',
            gv.VILLAGE_NAME Village,
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
            qd.equipments_setup_handling,
            qd.context_setting,
            qd.introduce_topic,
            qd.paused_video,
            qd.encouraged_adoption,
            qd.summarized_video,
            qd.subject_knowledge,
            qd.filled_dissemination,
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
        GROUP BY YEAR(qd.date) , MONTH(qd.date) , gc.id , gs.id , gd.id , gb.id , gv.id , vv.id
        ORDER BY YEAR(qd.date) DESC , MONTH(qd.date) DESC
        '''

        adoption_verification_query = '''SELECT
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
        GROUP BY YEAR(af.verification_date) , MONTH(af.verification_date) , gc.id , gs.id , gd.id , gb.id , gv.id , vv.id , pp.id , af.verification_date
        ORDER BY YEAR(af.verification_date) DESC , MONTH(af.verification_date) DESC
        '''

        adoption_verification_nonnego_query = '''SELECT
            af.id 'af_id',
            GROUP_CONCAT(IF(ann.adopted = '1', 'Yes', 'No')) 'Non Negotiable Adopted'
        FROM
            qacoco_adoptionverification af
                JOIN
            qacoco_adoptionnonnegotiableverfication ann ON af.id = ann.adoptionverification_id
            group by af.id
        '''

        video_quality_df = self.run_query(video_quality_query)
        dissemination_quality_df = self.run_query(dissemination_quality_query)
        adoption_verification_df = self.run_query(adoption_verification_query)
        adoption_verification_nonnego_df = self.run_query(adoption_verification_nonnego_query)
        combine_df = pd.merge(adoption_verification_df, adoption_verification_nonnego_df, how='inner')
        combine_df = combine_df.drop('af_id', axis=1)
        video_quality_df.to_csv(file_save_path+"video_quality_review.csv", sep=',', encoding='utf-8', index=False)
        dissemination_quality_df.to_csv(file_save_path+"dissemination_quality.csv", sep=',', encoding='utf-8', index=False)
        combine_df.to_csv(file_save_path+"adoption_verification.csv", sep=',', encoding='utf-8', index=False)
        self.send_mail([file_save_path+"video_quality_review.csv",file_save_path+"dissemination_quality.csv",file_save_path+"adoption_verification.csv"])
