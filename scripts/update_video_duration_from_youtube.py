import site, sys
sys.path.append('/home/ubuntu/code/dg_git')
site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)


import gdata.youtube.service

from datetime import timedelta, date
from smtplib import SMTP
from dashboard.models import *


yt_service = gdata.youtube.service.YouTubeService()

#Developer key of rahul@digitalgreen.org
yt_service.developer_key = 'AI39si74a5fwzrBsgSxjgImSsImXHfGgt8IpozLxty9oGP7CH0ky4Hf1eetV10IBi2KlgcgkAX-vmtmG86fdAX2PaG2CQPtkpA'
# The YouTube API does not currently support HTTPS/SSL access.
yt_service.ssl = False

error_ids = {}
filter_all = (date.today().day) % 7 == 0  #Check all videos every 7 days. Daily check for new videos only.
if filter_all:
    vids = Video.objects.exclude(youtubeid='')
else:
    vids = Video.objects.exclude(youtubeid='').filter(duration=None)

for vid in vids:
    try:
        #Fetch the video entry from Youtube
        entry = yt_service.GetYouTubeVideoEntry(video_id=vid.youtubeid)
    except gdata.service.RequestError, inst:
        error_ids[vid.id] = inst
    else:
        duration = timedelta(seconds = int(entry.media.duration.seconds))
        if vid.duration != str(duration):
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
     
       
        
    
        
        
        
        

