import json, datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from geographies.models import District, Block
import pandas as pd
import MySQLdb
import pandas.io.sql as psql



def home(request):

    partner_new = ''
    state_new = ''
    district_new = ''
    block_new = ''
    
    partner = [request.POST.get("partner")]
    state = [request.POST.get("state")]
    district = [request.POST.get("district")]
    block = [request.POST.get("block")]  
    
    partner_chk = [request.POST.get("partner_chk")]
    state_chk = [request.POST.get("state_chk")]
    district_chk = [request.POST.get("district_chk")]
    block_chk = [request.POST.get("block_chk")]
    
    if(partner[0]=='' and partner_chk[0]!=None):
        partner_new = "null"  
    elif (len(partner)>0 and partner_chk[0]==None) or (len(partner)>0 and partner_chk[0]!=None):
        partner_new = partner[0]
    
    if(state[0]=='' and state_chk[0]!=None):
        state_new = "null"
    elif (len(state)>0 and state_chk[0]==None) or (len(state)>0 and state_chk[0]!=None):
        state_new = state[0]
        print state_new

    if(district[0]=='' and district_chk[0]!=None):
        district_new = "null"
    elif (len(district)>0 and district_chk[0]==None) or (len(district)>0 and district_chk[0]!=None):
        district_new = district[0]

    if(block[0]=='' and block_chk[0]!=None):
        block_new = "null"
    elif (len(block)>0 and block_chk[0]==None) or (len(block)>0 and block_chk[0]!=None):
        block_new = block[0]


    handle(partner_new, state_new, district_new, block_new)
    
    return render_to_response('raw_data_analytics/output.html', context_instance=RequestContext(request))


def handle(partner, state, district, block):
    try:
        whereClause = " 1=1 "
        groupbyClause = ' group by S.state_name'
        gflag = 0
        sflag = 0
        selectClause = ''

        if len(partner)>0:
            if gflag == 1:
                groupbyClause += ',P.partner_name'
            else:
                gflag = 1
                groupbyClause = ' group by P.partner_name'
            if sflag == 1:
                selectClause += ',P.partner_name '
            else:
                sflag = 1
                selectClause = ' P.partner_name'
            if (partner!='null'):
                whereClause += "and P.partner_name=\'"+str(partner)+"\'"

        if len(state)>0:
            if gflag == 1:
                groupbyClause += ',S.state_name'
            else:
                gflag = 1
                groupbyClause = ' group by S.state_name'
            if sflag == 1:
                selectClause += ',S.state_name '
            else:
                sflag = 1
                selectClause = ' S.state_name'
            if (state!='null'):
                whereClause += "and S.state_name=\'"+str(state)+"\'"

        if len(district)>0:
            if gflag==1:
                groupbyClause += ',D.district_name'
            else:
                gflag = 1
                groupbyClause = ' group by D.district_name'
            if sflag == 1:
                selectClause += ',D.district_name '
            else:
                sflag = 1
                selectClause = ' D.district_name'
            if(district!='null'):
                whereClause += "and D.district_name=\'"+str(district)+"\'"

        if len(block)>0:
            if gflag == 1:
                groupbyClause += ',B.block_name'
            else:
                gflag = 1
                groupbyClause = ' group by B.block_name'
            if sflag == 1:
                selectClause += ',B.block_name '
            else:
                sflag = 1
                selectClause = ' B.block_name'
            if(block!='null'):
                whereClause += "and B.block_name=\'"+str(block)+"\'"

        execute(selectClause, whereClause, groupbyClause)
    except Exception as e:
        print e

def execute(selectClause, whereClause, groupbyClause):
    try:
        mysql_cn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='digitalgreen')
        Screeningquery = 'select'+ selectClause + ',count(SC.id) as nScreenings from activities_screening SC join programs_partner P on P.id=SC.partner_id join geographies_village V on SC.village_id=V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id where' + whereClause + groupbyClause + ';'

        Adoptionquery = 'select' + selectClause + ',count(ADP.id) as nAdoptions from activities_personadoptpractice ADP join programs_partner P on P.id=ADP.partner_id join people_person PP on ADP.person_id=PP.id join geographies_village V on PP.village_id = V.id join geographies_block B on V.block_id=B.id join geographies_district D on B.district_id=D.id join geographies_state S on D.state_id=S.id where' + whereClause + groupbyClause + ';'

        df_mysql_screening = psql.read_sql(Screeningquery, con=mysql_cn)

        df_mysql_adoption = psql.read_sql(Adoptionquery, con=mysql_cn)

        df_mysql = pd.merge(df_mysql_screening,df_mysql_adoption, how='outer')
        print 'loaded dataframe from MySQL. records:', len(df_mysql)
        print Screeningquery
        print "################################"
        print Adoptionquery
        print "################################"
        print df_mysql
        mysql_cn.close()
    except Exception as er:
        print er
    
