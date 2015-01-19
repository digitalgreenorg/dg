__author__ = 'Lokesh'
from management.commands import partition_library
from django.core import management

partition={'partner':partner, 'country':country, 'state':state, 'district':district, 'block':block, 'village':village}
value = {'nScreening':screening, 'nAdoption':adoption}
print "in views-------------------"
print partition
print "----- inside the views----------------"
print value
management.call_command('test_lib',from_date, to_date, partition=partition,value=value)
