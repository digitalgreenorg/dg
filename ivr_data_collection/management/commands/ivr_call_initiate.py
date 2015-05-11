from xml.dom import minidom
from django.core.management.base import BaseCommand
import time

import csv, os, logging, json, requests

sid = "digitalgreen2"
token = "421c11b1235067ca30ca87590c80c31eadc46af0"
        # agent_no="9718935868",
        #customerNo="9718935868",
customerNo="9910338592"
callerid="01130018178"
url='http://my.exotel.in/exoml/start/27037'
timelimit="500"  # This is optional
timeout="500" # This is also optional
calltype="trans" # Can be "trans" for transactional and "promo" for promotional content

class Command(BaseCommand):
    def call_exotel(self, mobile_number, video_id, person_id):
        r = requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'.format(sid=sid),
            auth=(sid, token),
            data={
                'From': int(mobile_number),
                'CallerId': callerid,
                'TimeLimit': timelimit,
                'Url': url,
                'TimeOut': timeout,
                'CallType': calltype,
                'CustomField': video_id
            })
        json_data = json.loads(r.text)
        logger = logging.getLogger('ivr_log')
        log_string = "".join(["Call begins : Call id : ", json_data['Call']['Sid'],", Person id : ",person_id, " , videoId : ", video_id])
        logger.debug(log_string)
        return True
    
    def handle(self, *args, **options):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        csvfile = open(os.path.join(__location__, 'test.csv'), 'rU')
        reader = csv.DictReader(csvfile)
        count = 0
        for row in reader:
            count=count+1
            if(count%10 == 0):
                time.sleep(300)
            self.call_exotel(row['Mobile_Number'],row['Video_ID'],row['Person_ID'])
