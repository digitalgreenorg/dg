import os, sys, site
site.addsitedir('/home/ubuntu/.virtualenv/dg_prod/lib/python2.7/site-packages/')
sys.path.append('/home/ubuntu/code/dg')
#import newrelic.agent
#newrelic.agent.initialize('/home/ubuntu/newrelic/newrelic-1.4.0.137/newrelic.ini')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dg.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
