from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'sandbox', settings.ROOT_URLCONF, name='sandbox'),  # <-- The `name` we used to in the `DEFAULT_HOST` setting
    host(r'beta', 'loop.urls', name='beta'),
)