"""
Run "python test_script.py"
Prints pass or fail for each test.
"""
from django.core.management import setup_environ
import settings
setup_environ(settings)

from dashboard.test_script import TestOfflineUser

print "Testing dashboard.OfflineUser ..."
TestOfflineUser().test_get_offline_pk()
TestOfflineUser().test_set_offline_pk()
