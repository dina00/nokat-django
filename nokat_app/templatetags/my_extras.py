from django import template

register = template.Library()
@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]
