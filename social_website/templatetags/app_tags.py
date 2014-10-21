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


@register.filter(name='placeholder')
def html_placeholder(field, args=None):
    if args == None:
        return field
    field.field.widget.attrs.update({"placeholder": args})
    field.field.widget.attrs.update({"class": 'auth'})
    return field

@register.filter(name='blog_desc')
def blog_desc(string):
    if(string.find("iframe")>=0):
        list_str = list(str(string))
        x = string.find('width')
        list_str[x+7] = '7'
        list_str[x+8] = '0'
        list_str[x+9] = '8'
        y = string.find('height')
        list_str[y+8] = '2'
        list_str[y+9] = '4'
        list_str[y+10] = '0'
        print ''.join(list_str)
        return ''.join(list_str)
    else:
        return str
