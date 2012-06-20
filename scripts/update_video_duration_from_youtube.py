import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')
import gdata.youtube
import gdata.youtube.service
from django.core.management import setup_environ
from datetime import timedelta
import settings
from smtplib import SMTP
setup_environ(settings)
from dashboard.models import *


yt_service = gdata.youtube.service.YouTubeService()

# The YouTube API does not currently support HTTPS/SSL access.
yt_service.ssl = False
error_ids = {}
vids = Video.objects.exclude(youtubeid='').filter(duration=None)
for vid in vids:
    try:
        #Fetch the video entry from Youtube
        entry = yt_service.GetYouTubeVideoEntry(video_id=vid.youtubeid)
    except gdata.service.RequestError, inst:
        error_ids[vid.id] = inst
    else:
        duration = timedelta(seconds = int(entry.media.duration.seconds))
        vid.duration = str(duration)
        vid.save()

#If there are errros in the youtube ID. Send mail to rahul@digitalgreen.org using SMTP on GMAIL
if(len(error_ids)> 0):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    
    serv = smtplib.SMTP("smtp.gmail.com",587)
    serv.ehlo()
    serv.starttls()
    serv.login("server@digitalgreen.org","virtuala")
    msg = MIMEMultipart()

    msg['From'] = 'server@digitalgreen.org'
    msg['To'] = 'rahul@digitalgreen.org'
    msg['Subject'] = 'Error in Youtube IDs in Database'
    
    text = ["Following Videos (ID & Error given) have problem with youtube id."]
    for k,v in error_ids.iteritems():
        text.append(str(k)+"\t"+str(v))
    msg.attach(MIMEText('\n'.join(text)))
    serv.sendmail('server@digitalgreen.org', 'rahul@digitalgreen.org', msg.as_string())
    
    serv.quit()
     
       
        
    
        
        
        
        

