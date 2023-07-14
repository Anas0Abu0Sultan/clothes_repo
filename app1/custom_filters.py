from django import template

register = template.Library()

@register.filter
def float_mul(value, arg):
    return float(value) * float(arg)
