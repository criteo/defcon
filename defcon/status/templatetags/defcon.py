"""Template tags for defcon."""
from django import template


register = template.Library()


@register.filter
def defcon_to_class(value):
    """Convert a defcon status to a bootstrap message level."""
    MAP = {
        5: 'success',
        4: 'info',
        3: 'warning',
        2: 'danger',
        1: 'danger'
    }
    return MAP.get(value, 'unknown')


@register.filter
def defcon_to_word(value):
    """Convert a defcon status to a bootstrap message level."""
    MAP = {
        5: 'good',
        4: 'normal',
        3: 'warning',
        2: 'danger',
        1: 'panic'
    }
    return MAP.get(value, 'unknown')


@register.filter
def defcon_to_color(value):
    """Convert a defcon status to a bootstrap message level."""
    MAP = {
        5: '#97CA00',
        4: '#a4a61d',
        3: '#dfb317',
        2: '#fe7d37',
        1: '#e05d44',
    }
    return MAP.get(value, 'unknown')
