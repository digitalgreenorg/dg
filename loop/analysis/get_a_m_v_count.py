import sys
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
application = get_wsgi_application()

import pandas as pd
from loop.models import CombinedTransaction, Mandi, LoopUser, DayTransportation, TransportationVehicle

def get_count():
    print "Getting count"
    df_dt = pd.DataFrame(list(DayTransportation.objects.filter(mandi__district__state=1).values('user_created_id','mandi__id','mandi__mandi_name_en','transportation_vehicle__vehicle__vehicle_name_en','transportation_vehicle__vehicle__id').order_by('-date')))
    df_loopuser = pd.DataFrame(list(LoopUser.objects.values('user__id','name_en')))

    df_dt = pd.merge(df_dt,df_loopuser,left_on='user_created_id',right_on='user__id',how='left')

    df_dt = df_dt.rename(columns={'mandi__mandi_name_en':'mandi_name','transportation_vehicle__vehicle__vehicle_name_en':'vehicle_name', 'transportation_vehicle__vehicle__id':'vehicle_id'})
    df_dt.drop(['user_created_id'],axis=1,inplace=True)
    print df_dt.head(n=10)



if __name__=="__main__":
    get_count()
