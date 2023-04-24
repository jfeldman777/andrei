from django import template
from ..models import Role


register = template.Library()

@register.filter
def isnumeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False




@register.filter
def isNotRole(value):
    if type(value) != Role:
        return True
    else:
        return False

# @register.filter
# def isObject(value):
#     if type(value) == str or float or int:
#         return False
#     return True


@register.filter
def isObject(value):
    if isinstance(value, (list, dict, tuple)):
        return True
    return False

@register.filter(name='increment')
def increment(value, amount=1):
    return value + amount

@register.filter
def in_list(value, arg):
    """Check if value is present in a comma-separated list."""
    return str(value) in arg.split(',')


@register.filter
def gt(value,x):
    if (value) <=x:
        return False
    return True
