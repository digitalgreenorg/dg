
from django.template.context import Context
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives
from django.conf import *
from dg.settings import EMAIL_HOST_USER
#-------------------------------------------------------------------------------
def common_send_email(subject, recipients, file, bcc=[], from_email=None):
    """
    This method is a common method to send email via the bhane system.
    """

    if not from_email:
        from_email = EMAIL_HOST_USER

    #get templates from file system
    attach_file_name = os.getcwd() + '/'+ file
    text_content = 'This is an important message.'

    #render the raw data in the template
    html_content = "ATTACHING Excel" 

    #contstruct the message and send it
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    msg.attach_file(attach_file_name)
    msg.send()


def set_columns_width(ws_obj):
    ws_obj.set_column('A:A',15)
    ws_obj.set_column('B:B',15)
    ws_obj.set_column('C:C',15)
    ws_obj.set_column('D:D',15)
    ws_obj.set_column('E:E',15)
    ws_obj.set_column('F:F',15)
    ws_obj.set_column('G:G',15)
    ws_obj.set_column('H:H',15)
    return ws_obj



def write_headers_in_sheet(ws_obj, format_str):
        ws_obj.write('A1', 'Sno', format_str)
        ws_obj.write('B1', 'Aggregator', format_str)
        ws_obj.write('C1', 'Village', format_str)
        ws_obj.write('D1', 'Farmer_ID', format_str)
        ws_obj.write('E1', 'Farmer', format_str)
        ws_obj.write('F1', 'Mobile Number', format_str)
        ws_obj.write('G1', 'Farmer Frequency', format_str)
        ws_obj.write('H1', 'Mobile Number Frequency', format_str)
        return ws_obj

    
def write_data_in_sheet(ws_obj, sheet_data):
        row = 1
        for item in sheet_data:
            col = 0
            item = list(item)
            item.insert(0, row)
            for sub_item in item:
                ws_obj.write(row, col, sub_item)
                col += 1
            row += 1

        return ws_obj 