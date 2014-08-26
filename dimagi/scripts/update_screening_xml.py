from dimagi.models import error_list
from xml.dom import minidom

from dimagi.models import XMLSubmission
from dimagi.scripts import save_mobile_data

xml_data = XMLSubmission.objects.filter(error_code=-5)

for obj in xml_data:
    xml_string = obj.xml_data
    xml_parse = minidom.parseString(xml_string)
    status = error_list['SUCCESS']
    msg = "No error."
    if xml_parse.getElementsByTagName('data'):
        data = xml_parse.getElementsByTagName('data')
        if data[0].attributes["name"].value.lower() == 'screening form' :
            status, msg = save_mobile_data.save_screening_data(xml_parse)
        elif data[0].attributes["name"].value.lower() == 'adoption form' :
            status, msg = save_mobile_data.save_adoption_data(xml_parse)
    elif xml_parse.getElementsByTagName('device_report'):
        status = error_list['DEVICE_REPORT']
        msg = 'device_report'
    else:
        status = error_list['UNIDENTIFIED_FORM']
        msg = 'Unidentified form. No data tag.'
    print status, msg
    obj.error_code = status
    obj.error_message = msg
    obj.save()
