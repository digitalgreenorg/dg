 # -*- coding: utf-8 -*-

#Code snippet ad imports for email attachment with encodings. To be used in another file for attachmnet in emails 

from django.template.context import Context
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives
import mimetypes
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
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

header_dict_for_loop_email_mobile_numbers = [{'column_width': 5,
                                          'label': 'क्रम संख्या',
                                          },
                                         {'column_width': 13,
                                          
                                          'label': 'जमाकर्ता का नाम',
                                          },
                                         {'column_width': 12,
                                          'label': 'गांव का नाम',
                                          },
                                         {'column_width': 8,
                                          'label': 'किसान ID',
                                          },
                                         {'column_width': 15,
                                          'label': 'किसान का नाम',
                                          },
                                          {'column_width': 8,
                                          'label': 'सब्जी कितने दिन दी?',
                                          },
                                         {'column_width': 10,
                                          'label': 'मोबाइल नं',
                                          },
                                         {'column_width': 10,
                                          'label': 'कितने किसान में नंबर डला है?',
                                          }]


query_for_all_aggregator = '''SELECT 
                              Aggregator,
                              Village,
                              Farmer_ID,
                              Farmer,
                              t1.Farmer_Frequency,
                              Mobile_Number,
                              t3.Mobile_Frequency
                          FROM
                              (SELECT 
                                  user_created_id,
                                      farmer_id f_id,
                                      COUNT(DISTINCT (date)) Farmer_Frequency
                              FROM
                                  loop_combinedtransaction lct
                              WHERE
                                  lct.date BETWEEN %s AND %s
                              GROUP BY user_created_id , farmer_id
                              HAVING Farmer_Frequency > 0) t1
                                  JOIN
                              (SELECT 
                                  ll.name Aggregator,
                                      ll.id Loop_user_id,
                                      ll.user_id user_id,
                                      lv.village_name Village,
                                      lf.id Farmer_ID,
                                      lf.name Farmer,
                                      lf.phone Mobile_Number
                              FROM
                                  loop_loopuser ll
                              JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
                              JOIN loop_farmer lf ON lf.village_id = llv.village_id
                              JOIN loop_village lv ON lf.village_id = lv.id
                              WHERE
                                  ll.name_en <> 'Loop Test') t2 ON t1.f_id = t2.Farmer_ID
                                  AND t1.user_created_id = t2.user_id
                                  JOIN
                              (SELECT 
                                      ll.user_id Loop_user,
                                      lf.phone Phone_no,
                                      COUNT(lf.phone) Mobile_Frequency
                              FROM
                               loop_loopuser ll join
                                  loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
                              JOIN loop_farmer lf ON lf.village_id = llv.village_id
                              JOIN loop_village lv ON lf.village_id = lv.id
                              WHERE
                                  llv.loop_user_id <> 22
                                      AND lf.id IN (SELECT 
                                          farmer_id
                                      FROM
                                          loop_combinedtransaction ct
                                      WHERE
                                      user_created_id=ll.user_id and
                                          date BETWEEN %s AND %s )
                              GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
                                  AND t3.Loop_user = t2.user_id
                          HAVING (t3.Mobile_Frequency > 1)
                              OR (t3.Mobile_Frequency = 1
                              AND (Mobile_Number <= 7000000000
                              OR Mobile_Number >= 9999999999))
                          ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''



query_for_single_aggregator = '''SELECT 
                                Aggregator,
                                Village,
                                Farmer_ID,
                                Farmer,
                                t1.Farmer_Frequency,
                                Mobile_Number,
                                t3.Mobile_Frequency
                            FROM
                                (SELECT 
                                    user_created_id,
                                        farmer_id f_id,
                                        COUNT(DISTINCT (date)) Farmer_Frequency
                                FROM
                                    loop_combinedtransaction lct
                                WHERE
                                    lct.date BETWEEN %s AND %s
                                GROUP BY user_created_id , farmer_id
                                HAVING Farmer_Frequency > 0) t1
                                    JOIN
                                (SELECT 
                                    ll.name Aggregator,
                                        ll.id Loop_user_id,
                                        ll.user_id user_id,
                                        lv.village_name Village,
                                        lf.id Farmer_ID,
                                        lf.name Farmer,
                                        lf.phone Mobile_Number
                                FROM
                                    loop_loopuser ll
                                JOIN loop_loopuserassignedvillage llv ON ll.id = llv.loop_user_id
                                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                JOIN loop_village lv ON lf.village_id = lv.id
                                WHERE
                                    ll.name_en <> 'Loop Test' and ll.name = \'%s\') t2 ON t1.f_id = t2.Farmer_ID
                                    AND t1.user_created_id = t2.user_id
                                    JOIN
                                (SELECT 
                                        ll.user_id Loop_user,
                                        lf.phone Phone_no,
                                        COUNT(lf.phone) Mobile_Frequency
                                FROM
                                 loop_loopuser ll join
                                    loop_loopuserassignedvillage llv on ll.id=llv.loop_user_id
                                JOIN loop_farmer lf ON lf.village_id = llv.village_id
                                JOIN loop_village lv ON lf.village_id = lv.id
                                WHERE
                                    llv.loop_user_id <> 22
                                        AND lf.id IN (SELECT 
                                            farmer_id
                                        FROM
                                            loop_combinedtransaction ct
                                        WHERE
                                        user_created_id=ll.user_id and
                                            date BETWEEN %s AND %s )
                                GROUP BY ll.user_id , lf.phone ) t3 ON t2.Mobile_Number = t3.Phone_no
                                    AND t3.Loop_user = t2.user_id
                            HAVING (t3.Mobile_Frequency > 1)
                                OR (t3.Mobile_Frequency = 1
                                AND (Mobile_Number <= 7000000000
                                OR Mobile_Number >= 9999999999))
                            ORDER BY Aggregator ASC, CAST(Mobile_Number AS signed) ASC'''


RECIPIENTS = ['amandeep@digitalgreen.org']

