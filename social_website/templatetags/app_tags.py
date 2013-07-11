from django import template

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