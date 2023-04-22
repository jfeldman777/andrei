from django import template

register = template.Library()

@register.filter
def isnumeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
