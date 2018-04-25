# -*- coding: utf-8 -*-

from django.core.mail.message import EmailMultiAlternatives
import mimetypes
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from django.core.mail.message import DEFAULT_ATTACHMENT_MIME_TYPE

# Code snippet ad imports for email attachment with encodings. To be used in another file for attachment in emails
# EmailMultiAlternatives included to provide support to alternative body content like HTML_TEXT

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


# Extra variables required in other files
DEFAULT_COLUMN_WIDTH = 9

header_dict_for_loop_email_mobile_numbers = {
    'workbook_name': u'%s/loop/Incorrect Mobile Numbers_%s_%s to %s.xlsx',
    'workbook_name_per_district': u'%s/loop/%s_Incorrect Mobile Numbers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_गलत मोबाइल नंबर की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 3.36,
                           'header': u'क्रम',
                           'col_seq': 'A:A',
                          },
                          {'column_width': 14.36,
                           'header': u'जमाकर्ता का\n नाम',
                           'col_seq': 'B:B',
                          },
                          {'column_width': 12,
                           'header': u'गांव का नाम',
                           'col_seq': 'C:C',
                          },
                          {'column_width': 6.36,
                           'header': u'किसान ID',
                           'col_seq': 'D:D',
                          },
                          {'column_width': 15,
                           'header': u'किसान का नाम',
                           'col_seq': 'E:E',
                          },
                          {'column_width': 8,
                           'header': u'सब्जी कितने\n दिन दी?',
                           'col_seq': 'F:F',
                          },
                          {'column_width': 10,
                           'header': u'मोबाइल नं',
                           'col_seq': 'G:G',
                          },
                          {'column_width': 11.27,
                           'header': u'कितने किसान\n में नंबर डला है?',
                           'col_seq': 'H:H',
                          }],
    'column_properties_district_wise': [{'column_width': 3.36,
                                         'header': u'क्रम',
                                         'col_seq': 'A:A',
                                        },
                                        {'column_width': 14.36,
                                         'header': u'जिला का\n नाम',
                                         'col_seq': 'B:B',
                                        },
                                        {'column_width': 14.36,
                                         'header': u'जमाकर्ता का\n नाम',
                                         'col_seq': 'B:B',
                                        },
                                        {'column_width': 12,
                                         'header': u'गांव का नाम',
                                         'col_seq': 'C:C',
                                        },
                                        {'column_width': 6.36,
                                         'header': u'किसान ID',
                                         'col_seq': 'D:D',
                                        },
                                        {'column_width': 15,
                                         'header': u'किसान का नाम',
                                         'col_seq': 'E:E',
                                        },
                                        {'column_width': 8,
                                         'header': u'सब्जी कितने\n दिन दी?',
                                         'col_seq': 'F:F',
                                        },
                                        {'column_width': 10,
                                         'header': u'मोबाइल नं',
                                         'col_seq': 'G:G',
                                        },
                                        {'column_width': 11.27,
                                         'header': u'कितने किसान\n में नंबर डला है?',
                                         'col_seq': 'H:H',
                                        }]
}

header_dict_for_farmer_transaction = {
    'workbook_name': u'%s/loop/Farmer Transactions_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_बिक्री का रिकॉर्ड_%s to %s',
    'column_properties': [{'column_width': 3.64,
                           'header': u'क्रम',
                           'col_seq': 'A:A',
                          },

                          {'column_width': 9.82,
                           'header': u'तारीख',
                           'col_seq': 'B:B',
                          },

                          {'column_width': 11.55,
                           'header': u'मंडी का नाम',
                           'col_seq': 'C:C',
                          },

                          {'column_width': 15,
                           'header': u'किसान का नाम',
                           'col_seq': 'D:D',
                          },

                          {'column_width': 9.09,
                           'header': u'कुल वजन (कि.)',
                           'col_seq': 'E:E',
                          },

                          {'column_width': 7,
                           'header': u'राशि (रु)',
                           'col_seq': 'F:F',
                          },

                          {'column_width': 7.45,
                           'header': u'किसान का भाग (रु)',
                           'col_seq': 'G:G',
                          },

                          {'column_width': 8.36,
                           'header': u'कुल राशि (रु)',
                           'col_seq': 'H:H',
                          },

                          {'column_width': 5.91,
                           'header': u'✓/ X',
                           'col_seq': 'I:I',
                          },

                          {'column_width': 16.55,
                           'header': u'टिप्पडी',
                           'col_seq': 'J:J',
                          }]
}

header_dict_for_farmer_outlier = {
    'workbook_name': u'%s/loop/Farmer Share Outliers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_फार्मर शेर आउटलाइयर्स की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 9.09,
                           'header': 'Date',
                           'col_seq': 'A:A',
                           'data_type': 'Date'
                          },
                          {'column_width': 16.55,
                           'header': 'Aggregator',
                           'col_seq': 'B:B'
                          },
                          {'column_width': 14.64,
                           'header': 'Market',
                           'col_seq': 'C:C'
                          },
                          {'column_width': 7.55,
                           'header': 'Quantity',
                           'col_seq': 'D:D'
                          },
                          {'column_width': 8.55,
                           'header': 'Transport Cost',
                           'col_seq': 'E:E'
                          },
                          {'column_width': 6.09,
                           'header': 'Farmer Share',
                           'col_seq': 'F:F'
                          },
                          {'column_width': 6.0,
                           'header': 'Farmer Share Per KG',
                           'col_seq': 'G:G'
                          },
                          {'column_width': 12.0,
                           'header': 'Farmer Share/Transport Cost',
                           'col_seq': 'H:H'
                          }
    ]
}

header_dict_for_transport_outlier = {
    'workbook_name': u'%s/loop/Transport Share Outliers_%s_%s to %s.xlsx',
    'worksheet_name': u'%s_गाड़ी किराया आउटलाइयर्स की लिस्ट_%s to %s',
    'column_properties': [{'column_width': 10.64,
                           'header': 'Date',
                           'data_type': 'Date',
                           'col_seq': 'A:A'
                          },
                          {'column_width': 16,
                           'header': 'Aggregator',
                           'col_seq': 'B:B'
                          },
                          {'column_width': 14.55,
                           'header': 'Market',
                           'col_seq': 'C:C'
                          },
                          {'column_width': 7.55,
                           'header': 'Quantity',
                           'col_seq': 'D:D'
                          },
                          {'column_width': 12.73,
                           'header': 'Transport Cost',
                           'col_seq': 'E:E'
                          },
                          {'column_width': 7.45,
                           'header': 'Type',
                           'col_seq': 'F:F'
                          },
                          {'column_width': 11.2,
                           'header': 'Transport CPK',
                           'col_seq': 'G:G'
                          }
    ]
}

sms_text = {
    'farmer': {'hi': u'किसान', 'en': u"Farmer", 'bn': u'কৃষকের', 'mr': u'शेतकऱ्यांची', 'te': u'రైతు'},
    'aggregator': {'hi': u'जमाकर्ता', 'en': u"Aggregator", 'bn': u"जमाकर्ता", 'mr': u"जमाकर्ता", 'te': u'ఆగ్రిగేటర్'},
    'currency': {'hi': u"₹", 'en': u'Rs', 'bn': u"৳", 'mr': u'₹', 'te': u'₹'},
    'date': {'hi': "", 'en': "Farmer", 'bn': "", 'mr': "", 'te': ""},
    'loop_receipt': {'hi': u'लूप-रसीद', 'en': u'Loop Receipt', 'bn': u'লুপ রশিদ',
                     'mr': u'लूप-पावती', 'te': u'లూప్ రశీదు'},
    'total': {'hi': u'कुल राशि', 'en': u'Total', 'bn': u'মোট', 'mr': u'एकूण रक्कम', 'te':u'మొత్తం'},
    'bracket_open': {'default': '('},
    'bracket_close': {'default': ')'},
    'helpline_no': {'hi': u'हेल्पलाइन नं.', 'en':u'Helpline No.', 'bn':u'হেল্পলাইন নম্বর', 'mr':u'मदतीसाठी संपर्क: ', 'te': u'హెల్ప్ లైన్ నంబరు'},
    'ke_liye': {'hi': u'के लिए', 'en':u'for', 'bn': u' জন্য ', 'mr':u'च्या साठी ', 'te': u'కొరకు'},
    'ka kiraya': {'hi': u'का किराया :', 'en': u',Rent', 'bn': u' খাজনা : ', 'mr': u'चा भाडा :', 'te': u'కిరాయి'}

}



RECIPIENTS = ['lokesh@digitalgreen.org', 'loop@digitalgreen.org']

RECIPIENTS_TEMP = ['amandeep@digitalgreen.org']
