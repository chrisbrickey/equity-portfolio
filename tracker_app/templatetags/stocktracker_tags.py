from django import template
register = template.Library()

@register.filter(name='multiply')
def multiply(a, b):
    interim = float(a) * float(b)
    rounded_string = str(round(interim, 3))
    return rounded_string
