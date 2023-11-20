from django import template

register = template.Library()

@register.filter
def sort_with_zero_first(value, arg):
    return sorted(value, key=lambda x: (-1 if x.contract_number == 0 else 1, -x.contract_number))
