from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

from django.http import HttpResponse

from dg import settings

import gdata.spreadsheet.service

class Mail:
    def __init__(self, to, subject, text, html, reply_to=""): 
        self.smtp_server = settings.EMAIL_HOST
        self.sender = settings.EMAIL_HOST_USER
        self.sender_password = settings.EMAIL_HOST_PASSWORD
        self.receiver = to
        
        # Compose Email
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver
        
        if reply_to:
            self.msg.add_header('reply-to', reply_to)
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        self.msg.attach(MIMEText(text, 'plain'))
        self.msg.attach(MIMEText(html, 'html'))
    
    def send(self):
        self.smtp = smtplib.SMTP_SSL(self.smtp_server)
        self.smtp.login(self.sender, self.sender_password)
        self.smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        self.smtp.quit()
        
def event_registration(request):
    # Events email to send registrations
    events_email = "events@digitalgreen.org"
    
    email = request.POST["Email"]
    text = ""
    html = ""
    dict_write = {}
    for field, value in request.POST.items():
        if field==u'csrfmiddlewaretoken':
            continue
        text += "%s: %s\n" % (field, value)
        html += "%s: %s <br />" % (field, value)
        dict_write[(field.replace(" ", "-")).lower()] = value
    
    subject = "Registration for Digital Green Workshop"
    mail = Mail(to=events_email, subject=subject, text=text, html=html, reply_to=email)
    try:
        mail.send()
        message = "Form submitted successfully."
    except:
        # Oh no! Could not connect to SMTP server. What should we do?
        message = "Error sending message."
    
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = settings.EMAIL_HOST_USER
    spr_client.password = settings.EMAIL_HOST_PASSWORD
    spr_client.source = 'Event Registration'
    spr_client.ProgrammaticLogin()

    entry = spr_client.InsertRow(dict_write, '0AmZADH8mNg75dElxaW9hS1AtNmNFc2xKVzEwRDFRMWc', 'od6')
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        print "Insert row succeeded."
    else:
        print "Insert row failed."
    return HttpResponse(message)
