from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from dimagi.models import error_list
from xml.dom import minidom

from dimagi.models import XMLSubmission
from dimagi.scripts import save_mobile_data
from dimagi.scripts.exception_email import sendmail

xml_data = XMLSubmission.objects.filter(error_code = -2).values('xml_data')

for data in xml_data:
    #print data['xml_data']
    xml_string = data['xml_data']
    xml_parse = minidom.parseString(xml_string)
    status = error_list['SUCCESS']
    msg = "No error."
    if xml_parse.getElementsByTagName('data'):
        data = xml_parse.getElementsByTagName('data')
        try:
            if data[0].attributes["name"].value.lower() == 'screening form' :
                status, msg = save_mobile_data.save_screening_data(xml_parse)
            elif data[0].attributes["name"].value.lower() == 'adoption form' :
                status, msg = save_mobile_data.save_adoption_data(xml_parse)
        except Exception as ex:
            error = "Error in saving submission in update_screening_script " + str(ex)
            sendmail("Exception in Mobile COCO", error)
    elif xml_parse.getElementsByTagName('device_report'):
        status = error_list['DEVICE_REPORT']
        msg = 'device_report'
    else:
        status = error_list['UNIDENTIFIED_FORM']
        msg = 'Unidentified form. No data tag.'
    print status, msg