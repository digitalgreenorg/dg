 # -*- coding: utf-8 -*-

from django.template.context import Context
from django.template.loader import get_template
from django.core.mail.message import EmailMultiAlternatives
from django.conf import *
from dg.settings import EMAIL_HOST_USER
from loop.config import *
#-------------------------------------------------------------------------------

def common_send_email(subject, recipients, files, bcc=[], from_email=None, html="", text=""):
    """
    This method is a common method to send email via the bhane system.
    """

    if not from_email:
        from_email = EMAIL_HOST_USER
    #get templates from file system
    
    text_content = 'This is an important message.'

    #render the raw data in the template
    html_content = "ATTACHING Excel" 

    #contstruct the message and send it
    msg = EmailMultiAlternativesWithEncoding(subject, text, from_email, recipients)
    msg.attach_alternative(html, 'text/html')

    for file in files:
        attach_file_name = file
        msg.attach_file(attach_file_name)
    msg.send()
    return
