from django import template

register = template.Library()

@register.filter
def defcon_to_class(value):
    MAP = {
        5: 'success',
        4: 'infos',
        3: 'warning',
        2: 'error',
        1: 'error'
    }
    return MAP.get(value, 'unknown')
