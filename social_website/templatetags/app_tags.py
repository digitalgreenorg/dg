from django import template
import time

register = template.Library()
MILLION = 1000000.0
THOUSAND = 1000.0
ROUND = 1
@register.filter(name='custom_multiply')
def custom_multiply(a):
    return a*5

@register.filter(name='custom_truncate_number')
def custom_truncate_number(num):
    if(num > MILLION):
        return ((str(round((num / MILLION), 1))) + 'M')
    if(num > THOUSAND):
        return ((str(round((num / THOUSAND), 1))) + 'K')
    return num

@register.filter(name='seconds_to_duration')
def seconds_to_duration(seconds):
    if seconds >= 3600:
        return time.strftime('%H:%M:%S', time.gmtime(seconds))
    else:
        return time.strftime('%M:%S', time.gmtime(seconds))