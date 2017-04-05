 # -*- coding: utf-8 -*-

#Code snippet ad imports for email attachment with encodings. To be used in another file for attachmnet in emails

from django.template.context import Context
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives
import mimetypes
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from dg.settings import EXOTEL_ID, EXOTEL_TOKEN, EXOTEL_HELPLINE_NUMBER, MEDIA_ROOT

from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE

class EmailMultiAlternativesWithEncoding(EmailMultiAlternatives):
    def _create_attachment(self, filename, content, mimetype=None):
        """
        Converts the filename, content, mimetype triple into a MIME attachment
        object. Use self.encoding when handling text attachments.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            encoding = self.encoding or settings.DEFAULT_CHARSET
            attachment = SafeMIMEText(smart_str(content,
                settings.DEFAULT_CHARSET), subtype, encoding)
        else:
            # Encode non-text attachments with base64.
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)
        if filename:
            try:
                filename = filename.encode('ascii')
            except UnicodeEncodeError:
                filename = Header(filename, 'utf-8').encode()
            attachment.add_header('Content-Disposition', 'attachment',
                                   filename=filename)
        return attachment





#Extra variables required in other files
DEFAULT_COLUMN_WIDTH = 9

header_dict_for_loop_email_mobile_numbers = {
     'workbook_name': u'%s/loop/Incorrect Mobile Numbers_%s_%s to %s.xlsx',
     'worksheet_name': u'%s_गलत मोबाइल नंबर की लिस्ट_%s to %s',
     'column_properties' : [{'column_width': 5,
                            'header': u'क्रम संख्या',
                            'col_seq':'A:A',
                           },
                           {'column_width': 13,
                            'header': u'जमाकर्ता का नाम',
                            'col_seq':'B:B',
                           },
                           {'column_width': 12,
                            'header': u'गांव का नाम',
                            'col_seq':'C:C',
                           },
                           {'column_width': 8,
                            'header': u'किसान ID',
                            'col_seq':'D:D',
                           },
                           {'column_width': 15,
                            'header': u'किसान का नाम',
                            'col_seq':'E:E',
                           },
                           {'column_width': 8,
                            'header': u'सब्जी कितने दिन दी?',
                            'col_seq':'F:F',
                           },
                           {'column_width': 10,
                            'header': u'मोबाइल नं',
                            'col_seq':'G:G',
                           },
                           {'column_width': 10,
                            'header': u'कितने किसान में नंबर डला है?',
                            'col_seq':'H:H',
                           }]
     }


header_dict_for_farmer_transaction = [{'column_width': 3.64,
                                          'label': 'क्रम',
                                          },
                                         {'column_width': 9.82,

                                          'label': 'तारीख',
                                          },
                                         {'column_width': 11.55,
                                          'label': 'मंडी का नाम',
                                          },
                                         {'column_width': 15,
                                          'label': 'किसान का नाम',
                                          },
                                         {'column_width': 9.09,
                                          'label': 'कुल वजन (कि.)',
                                          },
                                          {'column_width': 7,
                                          'label': 'राशि (रु)',
                                          },
                                         {'column_width': 7.45,
                                          'label': 'किसान का भाग (रु)',
                                          },
                                         {'column_width': 8.36,
                                          'label': 'कुल राशि (रु)',
                                          },
                                          {'column_width': 5.91,
                                          'label': '✓/ X',
                                          },
                                          {'column_width': 16.55,
                                          'label': 'टिप्पडी',
                                          }]



header_dict_for_transport_details = [{'column_width': 3.64,
                                          'label': 'क्रम संख्या',
                                          },
                                         {'column_width': 13 ,
                                          'label': 'जमाकर्ता का नाम',
                                          },
                                         {'column_width': 12,
                                          'label': 'तारीख',
                                          },
                                         {'column_width': 8,
                                          'label': 'मंडी का नाम',
                                          },
                                         {'column_width': 15,
                                          'label': 'गाड़ी मालिक',
                                          },
                                          {'column_width': 8,
                                          'label': 'गाड़ी नं',
                                          },
                                         {'column_width': 10,
                                          'label': 'गाड़ी का किराया (रु)',
                                          },
                                         {'column_width': 10,
                                          'label': '✓/ X',
                                          },
                                          {
                                          'column_width': 20,
                                          'label': 'टिप्पडी'
                                          }]


# query_for_incorrect_phone_no_all_aggregator = '''SELECT
#                               Aggregator,
#                               Village,
#                               Farmer_ID,
#                               Farmer,
#                               t1.Farmer_Frequency,
#                               Mobile_Number,
#                               t3.Mobile_Frequency
#                           FROM
#                               (SELECT
#                                   user_created_id,
#                                       farmer_id f_id,
#                                       COUNT(DISTINCT (date)) Farmer_Frequency
#                               FROM
#                                   loop_combinedtransaction lct
#                               WHERE
#                                   lct.date BETWEEN %s AND %s
#                               GROUP BY user_created_id , farmer_id
#                               HAVING Farmer_Frequency > 0) t1
#                                   JOIN
#                               (SELECT
#                                   ll.name Aggregator,
#                                       ll.id Loop_user_id,
#                                       ll.user_id user_id,
#                                       lv.village_name Village,
#                                       lf.id Farmer_ID,
#                                       lf.name Farmer,
#                                       lf.phone Mobile_Number
#                               FROM
#                                   loop_loopuser ll
#                               JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
#                               JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                               JOIN loop_village lv ON lf.village_id = lv.id
#                               WHERE
#                                   ll.role = 2) t2 ON t1.f_id = t2.Farmer_ID
#                                   AND t1.user_created_id = t2.user_id
#                                   JOIN
#                               (SELECT
#                                       ll.user_id Loop_user,
#                                       lf.phone Phone_no,
#                                       COUNT(lf.phone) Mobile_Frequency
#                               FROM
#                                loop_loopuser ll join
#                                   loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
#                               JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                               JOIN loop_village lv ON lf.village_id = lv.id
#                               WHERE
#                                   llv.loop_user_id <> 22
#                                       AND lf.id IN (SELECT
#                                           farmer_id
#                                       FROM
#                                           loop_combinedtransaction ct
#                                       WHERE
#                                       user_created_id=ll.user_id and
#                                           date BETWEEN %s AND %s )
#                               GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
#                                   AND t3.Loop_user = t2.user_id
#                           HAVING (t3.Mobile_Frequency > 1)
#                               OR (t3.Mobile_Frequency = 1
#                               AND (Mobile_Number <= 7000000000
#                               OR Mobile_Number >= 9999999999))
#                           ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''


#
# query_for_incorrect_phone_no_single_aggregator = '''SELECT
#                                 Aggregator,
#                                 Village,
#                                 Farmer_ID,
#                                 Farmer,
#                                 t1.Farmer_Frequency,
#                                 Mobile_Number,
#                                 t3.Mobile_Frequency
#                             FROM
#                                 (SELECT
#                                     user_created_id,
#                                         farmer_id f_id,
#                                         COUNT(DISTINCT (date)) Farmer_Frequency
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 WHERE
#                                     lct.date BETWEEN %s AND %s
#                                 GROUP BY user_created_id , farmer_id
#                                 HAVING Farmer_Frequency > 0) t1
#                                     JOIN
#                                 (SELECT
#                                     ll.name Aggregator,
#                                         ll.id Loop_user_id,
#                                         ll.user_id user_id,
#                                         lv.village_name Village,
#                                         lf.id Farmer_ID,
#                                         lf.name Farmer,
#                                         lf.phone Mobile_Number
#                                 FROM
#                                     loop_loopuser ll
#                                 JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
#                                 JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                                 JOIN loop_village lv ON lf.village_id = lv.id
#                                 WHERE
#                                     ll.role = 2 and ll.name_en= \'%s\') t2 ON t1.f_id = t2.Farmer_ID
#                                     AND t1.user_created_id = t2.user_id
#                                     JOIN
#                                 (SELECT
#                                         ll.user_id Loop_user,
#                                         lf.phone Phone_no,
#                                         COUNT(lf.phone) Mobile_Frequency
#                                 FROM
#                                  loop_loopuser ll join
#                                     loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
#                                 JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                                 JOIN loop_village lv ON lf.village_id = lv.id
#                                 WHERE
#                                     llv.loop_user_id <> 22
#                                         AND lf.id IN (SELECT
#                                             farmer_id
#                                         FROM
#                                             loop_combinedtransaction ct
#                                         WHERE
#                                         user_created_id=ll.user_id and
#                                             date BETWEEN %s AND %s )
#                                 GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
#                                     AND t3.Loop_user = t2.user_id
#                             HAVING (t3.Mobile_Frequency > 1)
#                                 OR (t3.Mobile_Frequency = 1
#                                 AND (Mobile_Number <= 7000000000
#                                 OR Mobile_Number >= 9999999999))
#                             ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''
#
#
# query_for_incorrect_phone_no_single_aggregator_new = '''SELECT
#                                 Aggregator,
#                                 Village,
#                                 Farmer_ID,
#                                 Farmer,
#                                 t1.Farmer_Frequency,
#                                 Mobile_Number,
#                                 t3.Mobile_Frequency
#                             FROM
#                                 (SELECT
#                                     user_created_id,
#                                         farmer_id f_id,
#                                         COUNT(DISTINCT (date)) Farmer_Frequency
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 WHERE
#                                     lct.date BETWEEN %s AND %s
#                                 GROUP BY user_created_id , farmer_id
#                                 HAVING Farmer_Frequency > 0) t1
#                                     JOIN
#                                 (SELECT
#                                     ll.name Aggregator,
#                                         ll.id Loop_user_id,
#                                         ll.user_id user_id,
#                                         lv.village_name Village,
#                                         lf.id Farmer_ID,
#                                         lf.name Farmer,
#                                         lf.phone Mobile_Number
#                                 FROM
#                                     loop_loopuser ll
#                                 JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
#                                 JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                                 JOIN loop_village lv ON lf.village_id = lv.id
#                                 WHERE
#                                     ll.role = 2) t2 ON t1.f_id = t2.Farmer_ID
#                                     AND t1.user_created_id = t2.user_id
#                                     JOIN
#                                 (SELECT
#                                         ll.user_id Loop_user,
#                                         lf.phone Phone_no,
#                                         COUNT(lf.phone) Mobile_Frequency
#                                 FROM
#                                  loop_loopuser ll join
#                                     loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
#                                 JOIN loop_farmer lf ON lf.village_id = llv.village_id
#                                 JOIN loop_village lv ON lf.village_id = lv.id
#                                 WHERE
#                                     llv.loop_user_id <> 22
#                                         AND lf.id IN (SELECT
#                                             farmer_id
#                                         FROM
#                                             loop_combinedtransaction ct
#                                         WHERE
#                                         user_created_id=ll.user_id and
#                                             date BETWEEN %s AND %s )
#                                 GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
#                                     AND t3.Loop_user = t2.user_id
#                             HAVING (t3.Mobile_Frequency > 1)
#                                 OR (t3.Mobile_Frequency = 1
#                                 AND (Mobile_Number <= 7000000000
#                                 OR Mobile_Number >= 9999999999))
#                             ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''
#
#
# query_for_farmer_transaction_all_aggregator = '''
#                                   SELECT
#                               t1.Agg,
#                               t1.date,
#                               t1.Mandi,
#                               t1.Farmer,
#                               Total_Quantity,
#                               Total_Amount,
#                               ts / tv * Total_Quantity fs,
#                               Total_Amount - (ts / tv * Total_Quantity) Net_Amount
#                           FROM
#                               (SELECT
#                                   lct.user_created_id Agg,
#                                       date,
#                                       lm.mandi_name Mandi,
#                                       lf.name Farmer,
#                                       SUM(quantity) Total_Quantity,
#                                       SUM(amount) Total_Amount
#                               FROM
#                                   loop_combinedtransaction lct
#                               JOIN loop_farmer lf ON lf.id = lct.farmer_id
#                               JOIN loop_mandi lm ON lct.mandi_id = lm.id
#                               GROUP BY Agg , date , Mandi , lct.farmer_id) t1
#                                   JOIN
#                               (SELECT
#                                   t2.user_ User_id,
#                                       t2.date Date_,
#                                       t2.mandi Mandi_,
#                                       t2.Total_Volume tv,
#                                       t3.Share_ ts
#                               FROM
#                                   (SELECT
#                                   lct.user_created_id user_,
#                                       date,
#                                       lm.mandi_name mandi,
#                                       SUM(quantity) Total_Volume
#                               FROM
#                                   loop_combinedtransaction lct
#                               JOIN loop_mandi lm ON lm.id = lct.mandi_id
#                               GROUP BY user_ , date , lct.mandi_id) t2
#                               JOIN (SELECT
#                                   dt.user_created_id,
#                                       date,
#                                       lm.mandi_name mandi_,
#                                       AVG(farmer_share) Share_
#                               FROM
#                                   loop_daytransportation dt
#                               JOIN loop_mandi lm ON dt.mandi_id = lm.id
#                               GROUP BY user_created_id , date , dt.mandi_id) t3 ON t2.user_ = t3.user_created_id
#                                   AND t2.date = t3.date
#                                   AND t2.mandi = t3.mandi_) t4 ON t1.Agg = t4.User_id
#                                   AND t1.date = t4.Date_
#                                   AND t1.Mandi = t4.Mandi_
#                           WHERE
#                               t1.date BETWEEN %s AND %s
#                         '''
#
#
# query_for_farmer_transaction_single_aggregator = '''
#                                   SELECT
#                                 t1.Agg,
#                                 t1.date,
#                                 t1.Mandi,
#                                 t1.Farmer,
#                                 Total_Quantity,
#                                 Total_Amount,
#                                 ts / tv * Total_Quantity fs,
#                                 Total_Amount - (ts / tv * Total_Quantity) Net_Amount
#                             FROM
#                                 (SELECT
#                                     lct.user_created_id Agg,
#                                         date,
#                                         lm.mandi_name Mandi,
#                                         lf.name Farmer,
#                                         SUM(quantity) Total_Quantity,
#                                         SUM(amount) Total_Amount
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 JOIN loop_farmer lf ON lf.id = lct.farmer_id
#                                 JOIN loop_mandi lm ON lct.mandi_id = lm.id
#                                 GROUP BY Agg , date , Mandi , lct.farmer_id) t1
#                                     JOIN
#                                 (SELECT
#                                     t2.user_ User_id,
#                                         t2.date Date_,
#                                         t2.mandi Mandi_,
#                                         t2.Total_Volume tv,
#                                         t3.Share_ ts
#                                 FROM
#                                     (SELECT
#                                     lct.user_created_id user_,
#                                         date,
#                                         lm.mandi_name mandi,
#                                         SUM(quantity) Total_Volume
#                                 FROM
#                                     loop_combinedtransaction lct
#                                 JOIN loop_mandi lm ON lm.id = lct.mandi_id
#                                 GROUP BY user_ , date , lct.mandi_id) t2
#                                 JOIN (SELECT
#                                     dt.user_created_id,
#                                         date,
#                                         lm.mandi_name mandi_,
#                                         AVG(farmer_share) Share_
#                                 FROM
#                                     loop_daytransportation dt
#                                 JOIN loop_mandi lm ON dt.mandi_id = lm.id
#                                 GROUP BY user_created_id , date , dt.mandi_id) t3 ON t2.user_ = t3.user_created_id
#                                     AND t2.date = t3.date
#                                     AND t2.mandi = t3.mandi_) t4 ON t1.Agg = t4.User_id
#                                     AND t1.date = t4.Date_
#                                     AND t1.Mandi = t4.Mandi_
#                             WHERE
#                                 t1.date BETWEEN %s AND %s
#                                     AND t1.Agg = %s'''
#
#
# query_for_transport_details_all_aggregator = '''
#                           SELECT
#                               ll.name Agg_Id,
#                               ct.date Date_,
#                               lm.mandi_name Mandi,
#                               lt.transporter_name T_name,
#                               tv.vehicle_number Vehicle_Num,
#                               AVG(dt.transportation_cost) Cost
#                           FROM
#                               loop_combinedtransaction ct
#                                   JOIN
#                               loop_daytransportation dt ON ct.user_created_id = dt.user_created_id
#                                   AND ct.mandi_id = dt.mandi_id
#                                   AND ct.date = dt.date
#                                   JOIN
#                               loop_transportationvehicle tv ON tv.id = dt.transportation_vehicle_id
#                                   JOIN
#                               loop_mandi lm ON lm.id = ct.mandi_id
#                                   JOIN
#                               loop_transporter lt ON lt.id = tv.transporter_id
#                                   JOIN
#                               loop_vehicle lv ON lv.id = tv.vehicle_id
#                                   JOIN
#                               loop_loopuser ll ON ll.user_id = ct.user_created_id
#                           WHERE
#                               ct.date BETWEEN %s AND %s AND ll.role = '2'
#                           GROUP BY Agg_Id , Date_ , ct.mandi_id , tv.transporter_id , Vehicle_Num
#                           '''
#
#
# query_for_transport_details_single_aggregator = '''
#                           SELECT
#                               ll.name Agg_Id,
#                               ct.date Date_,
#                               lm.mandi_name Mandi,
#                               lt.transporter_name T_name,
#                               tv.vehicle_number Vehicle_Num,
#                               AVG(dt.transportation_cost) Cost
#                           FROM
#                               loop_combinedtransaction ct
#                                   JOIN
#                               loop_daytransportation dt ON ct.user_created_id = dt.user_created_id
#                                   AND ct.mandi_id = dt.mandi_id
#                                   AND ct.date = dt.date
#                                   JOIN
#                               loop_transportationvehicle tv ON tv.id = dt.transportation_vehicle_id
#                                   JOIN
#                               loop_mandi lm ON lm.id = ct.mandi_id
#                                   JOIN
#                               loop_transporter lt ON lt.id = tv.transporter_id
#                                   JOIN
#                               loop_vehicle lv ON lv.id = tv.vehicle_id
#                                   JOIN
#                               loop_loopuser ll ON ll.user_id = ct.user_created_id
#                           WHERE
#                               ct.date BETWEEN %s AND %s AND ll.name = \'%s\' and ll.role = '2'
#                           GROUP BY Agg_Id , Date_ , ct.mandi_id , tv.transporter_id , Vehicle_Num
#                           '''



RECIPIENTS = ['lokesh@digitalgreen.org']

RECIPIENTS_TEMP = ['amandeep@digitalgreen.org']


