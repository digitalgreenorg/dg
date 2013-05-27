from django import template

register = template.Library()

@register.filter(name='custom_multiply')
def custom_multiply(a):
    print 'tanmay'
    print a*5
    return a*5