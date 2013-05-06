from django.core.management import setup_environ
import settings
setup_environ(settings)
import api
from dashboard.models import *

def get_user_villages_for_test(user_id):
    user_permissions = UserPermission.objects.filter(username = user_id)
    villages = Village.objects.none()
    for user_permission in user_permissions:
        if(user_permission.role=='A'):
            villages = villages | Village.objects.all()
        if(user_permission.role=='D'):
            states = State.objects.filter(region = user_permission.region_operated)
            districts = District.objects.filter(state__in = states)
            blocks = Block.objects.filter(district__in = districts)
            villages = villages | Village.objects.filter(block__in = blocks)
        if(user_permission.role=='F'):
            blocks = Block.objects.filter(district = user_permission.district_operated)
            villages = villages | Village.objects.filter(block__in = blocks)
    return villages

class test_pr(api.PersonResource):
    """
    >>> import urllib,urllib2, base64, json
    >>> from dashboard.models import *
    >>> request = urllib2.Request("http://127.0.0.1:8000/api/v1/person/?limit=0")
    >>> base64string = base64.b64encode('%s:%s' % ('sreenu', 'sreenivas'))
    >>> request.add_header("Authorization", "Basic %s" % base64string)
    >>> result = urllib2.urlopen(request)
    >>> data  = json.load(result)
    >>> id_list = []
    >>> for id in range(len(data['objects'])):
    ...     id_list.append(int(data['objects'][id]['id']))
    ...
    >>> villages = get_user_villages_for_test(35)
    >>> person_list = Person.objects.filter(village__in = villages).values_list('id', flat = True)
    >>> len(person_list) == len(id_list)
    True
    >>> request = urllib2.Request("http://127.0.0.1:8000/api/v1/person/")
    >>> base64string = base64.b64encode('digitalgreen:Green11017.')
    >>> request.add_header("Authorization", "Basic %s" % base64string)
    >>> request.add_header("Content-Type", "application/json")
    >>> data = json.dumps({"age":"23","father_name":"asd","gender":"M","person_name":"sdk","village":"/api/v1/village/10000000000251/"})
    >>> result = urllib2.urlopen(request, data)
    >>> result.getcode()
    201
    """
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()