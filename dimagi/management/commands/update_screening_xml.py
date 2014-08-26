from xml.dom import minidom
from django.core.management.base import BaseCommand

from dimagi.models import error_list, XMLSubmission
from dimagi.scripts import save_mobile_data
from dimagi.scripts.exception_email import sendmail

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        xml_data = XMLSubmission.objects.filter(error_code=-2)
        
        for obj in xml_data:
            xml_string = obj.xml_data
            xml_parse = minidom.parseString(xml_string)
            status = error_list['SUCCESS']
            msg = "success"
            if xml_parse.getElementsByTagName('data'):
                data = xml_parse.getElementsByTagName('data')
                try:
                    if data[0].attributes["name"].value.lower() == 'screening form' :
                        status, msg = save_mobile_data.save_screening_data(xml_parse)
                    elif data[0].attributes["name"].value.lower() == 'adoption form' :
                        status, msg = save_mobile_data.save_adoption_data(xml_parse)
                except Exception as ex:
                    error = "Error in update_screening_xml : " + str(ex)
                    sendmail("Exception in update_screening_xml", error)
            elif xml_parse.getElementsByTagName('device_report'):
                status = error_list['DEVICE_REPORT']
                msg = 'device_report'
            else:
                status = error_list['UNIDENTIFIED_FORM']
                msg = 'Unidentified form. No data tag.'
            print status, msg
            try:
                obj.error_code = status
                obj.error_message = msg
                obj.save()
            except Exception as ex:
                error = "Error in Updating XML Submission : " + str(ex)
                sendmail("Exception in update_screening_xml", error)