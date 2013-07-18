import site, sys
##For local migrations uncomment below lines
#sys.path.append('C:\Users\sreenu\Documents\gitdg')
##for server side testing
sys.path.append('/home/ubuntu/code/dg_coco_test/dg')
site.addsitedir('/home/ubuntu/.virtualenvs/dg_coco_testbed/lib/python2.7/site-packages/')

from django.core.management import setup_environ
import settings


setup_environ(settings)

from dashboard.models import *

for user in User.objects.all():
    user_permissions = UserPermission.objects.filter(username = user.id)
    villages = Village.objects.none()
    partner = None
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            villages = villages | Village.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
            districts = District.objects.filter(state__in = states)
            partner =  Partners.objects.filter(district__in = districts).values_list('id')
            partner = partner[0][0] if partner else None
            print 'partner for dm role', partner
            blocks = Block.objects.filter(district__in = districts)
            villages = villages | Village.objects.filter(block__in = blocks)
        if(user_permission.role=='F'):
            blocks = Block.objects.filter(district = user_permission.district_operated)
            try:
                partner = user_permission.district_operated.partner.id
            except:
                continue
            villages = villages | Village.objects.filter(block__in = blocks)
            partner = user_permission.district_operated.partner.id
    
    if partner:
        print user.id, partner
        try:
            obj, created = CocoUser.objects.get_or_create(user_id = user.id, partner_id = partner)
            i = 0
            for vil in villages:           
                if not vil in obj.villages.all():
                    obj.villages.add(vil)
                    i +=1
            print "user_id: " + str(user.id) +  " Added villages: " + str(i) +" , total villages"+ str(len(obj.villages.all()))
        
        except:
            print 'exception with user', user.id
            continue
        
    else:
        print 'partner does not exist for user: '+user.username 
