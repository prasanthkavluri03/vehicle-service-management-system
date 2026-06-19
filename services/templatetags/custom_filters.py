from django import template

register = template.Library()

# Custom multiplication filter for template values
@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0.0
