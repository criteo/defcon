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
