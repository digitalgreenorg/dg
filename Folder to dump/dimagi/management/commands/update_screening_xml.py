from xml.dom import minidom
from django.core.management.base import BaseCommand

from dimagi.models import error_list, XMLSubmission
from dimagi.scripts import save_mobile_data
from dimagi.scripts.exception_email import sendmail


class Command(BaseCommand):

    def handle(self, *args, **options):
        xml_data = XMLSubmission.objects.filter(error_code=-3)
        print len(xml_data)
        length = 0
        for obj in xml_data:
            length = length + 1
            xml_string = obj.xml_data
            xml_parse = minidom.parseString(xml_string)
            print "#" + str(obj.id)
            old_msg = obj.error_message
            old_code = obj.error_code
            status = error_list['SUCCESS']
            msg = "success"
            if xml_parse.getElementsByTagName('data'):
                data = xml_parse.getElementsByTagName('data')
                try:
                    if data[0].attributes["name"].value.lower() == 'screening form' or data[0].attributes["name"].value.lower() == 'screening form [en]':
                        status, msg = save_mobile_data.save_screening_data(xml_parse)
                    elif data[0].attributes["name"].value.lower() == 'adoption form' or data[0].attributes["name"].value.lower() == 'adoption form [en]':
                        status, msg = save_mobile_data.save_adoption_data(xml_parse)
                    else:
                        status = error_list['UNIDENTIFIED_FORM']
                        msg = 'Unidentified form. Data Tag with some other form name.'
                except Exception as ex:
                    error = "Error in update_screening_xml : " + str(ex)
                    sendmail("Exception in update_screening_xml", error)
            elif xml_parse.getElementsByTagName('device_report'):
                status = error_list['DEVICE_REPORT']
                msg = 'device_report'
            else:
                status = error_list['UNIDENTIFIED_FORM']
                msg = 'Unidentified form. No data tag.'
            try:
                obj.error_code = status
                obj.error_message = msg
                obj.save()
            except Exception as ex:
                error = "Error in Updating XML Submission : " + str(ex)
                sendmail("Exception in update_screening_xml", error)
            print old_msg, old_code, obj.error_message, obj.error_code
        print length
