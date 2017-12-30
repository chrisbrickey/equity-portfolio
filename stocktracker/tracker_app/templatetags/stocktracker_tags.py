from django import template
register = template.Library()

@register.filter(name='multiply')
def multiply(a, b):
    interim = float(a) * float(b)
    rounded_string = str(round(interim, 3))
    return rounded_string

@register.filter(name='market_value')
def market_value(a, b):
    interim = float(a) * float(b)
    rounded_string = str(round(interim, 3))
    return {'market_value': rounded_string}
