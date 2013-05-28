from django import template

register = template.Library()

@register.filter(name='custom_multiply')
def custom_multiply(a):
    return a*5